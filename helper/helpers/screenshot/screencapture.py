from os import fsync
from struct import pack
from zlib import crc32, compress
from sys import getwindowsversion
from ctypes import POINTER, WINFUNCTYPE, c_void_p
from ctypes import WinDLL, windll, Array, c_char, create_string_buffer, sizeof
from ctypes.wintypes import BOOL, DOUBLE, DWORD, HBITMAP, HDC, HGDIOBJ, HWND, INT, LPARAM, LPRECT, RECT, UINT
from threading import Lock, current_thread, main_thread
from typing import Any, Callable, List, Optional, Tuple, Union, Dict

from helper.helpers.screenshot.screen import Screen
from helper.helpers import BitmapInfoHeader, BitmapInfo

CAPTUREBLT = 0x40000000
DIB_RGB_COLORS = 0
SRCCOPY = 0x00CC0020
MONITORNUMPROC = WINFUNCTYPE(INT, DWORD, DWORD, POINTER(RECT), DOUBLE)
CFUNCTIONS = {
    "BitBlt": ("gdi32", [HDC, INT, INT, INT, INT, HDC, INT, INT, DWORD], BOOL),
    "CreateCompatibleBitmap": ("gdi32", [HDC, INT, INT], HBITMAP),
    "CreateCompatibleDC": ("gdi32", [HDC], HDC),
    "DeleteObject": ("gdi32", [HGDIOBJ], INT),
    "EnumDisplayMonitors": ("user32", [HDC, c_void_p, MONITORNUMPROC, LPARAM], BOOL),
    "GetDeviceCaps": ("gdi32", [HWND, INT], INT),
    "GetDIBits": ("gdi32", [HDC, HBITMAP, UINT, UINT, c_void_p, POINTER(BitmapInfo), UINT], BOOL),
    "GetSystemMetrics": ("user32", [INT], INT),
    "GetWindowDC": ("user32", [HWND], HDC),
    "SelectObject": ("gdi32", [HDC, HGDIOBJ], HGDIOBJ),
}

lock = Lock()


class Screencapture:

    bmp = None
    memdc = None
    Monitor = Dict[str, int]

    _srcdc_dict = {}

    def __init__(self, **_: Any):

        self.cls_image = Screen
        self.compression_level = 6
        self.with_cursor = False
        self._monitors = []

        self.user32 = WinDLL("user32")
        self.gdi32 = WinDLL("gdi32")
        self._set_cfunctions()
        self._set_dpi_awareness()

        self._bbox = {"height": 0, "width": 0}
        self._data: Array[c_char] = create_string_buffer(0)

        srcdc = self._get_srcdc()

        if not Screencapture.memdc:
            Screencapture.memdc = self.gdi32.CreateCompatibleDC(srcdc)

        bmi = BitmapInfo()
        bmi.bmiHeader.biSize = sizeof(BitmapInfoHeader)
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = 0
        bmi.bmiHeader.biClrUsed = 0
        bmi.bmiHeader.biClrImportant = 0

        self._bmi = bmi

    @property
    def monitors(self):

        if not self._monitors:
            with lock:
                self._monitors_impl()

        return self._monitors

    @staticmethod
    def _merge(screenshot: Screen, cursor: Screen):

        (cx, cy), (cw, ch) = cursor.position, cursor.size
        (x, y), (w, h) = screenshot.position, screenshot.size

        cx2, cy2 = cx + cw, cy + ch
        x2, y2 = x + w, y + h

        overlap = cx < x2 and cx2 > x and cy < y2 and cy2 > y

        if not overlap:
            return screenshot

        screen_data = screenshot.raw
        cursor_data = cursor.raw

        cy, cy2 = (cy - y) * 4, (cy2 - y2) * 4
        cx, cx2 = (cx - x) * 4, (cx2 - x2) * 4
        start_count_y = -cy if cy < 0 else 0
        start_count_x = -cx if cx < 0 else 0
        stop_count_y = ch * 4 - max(cy2, 0)
        stop_count_x = cw * 4 - max(cx2, 0)
        rgb = range(3)

        for count_y in range(start_count_y, stop_count_y, 4):
            pos_s = (count_y + cy) * w + cx
            pos_c = count_y * cw

            for count_x in range(start_count_x, stop_count_x, 4):
                spos = pos_s + count_x
                cpos = pos_c + count_x
                alpha = cursor_data[cpos + 3]

                if not alpha:
                    continue

                if alpha == 255:
                    screen_data[spos:spos + 3] = cursor_data[cpos: cpos + 3]

                else:
                    alpha = alpha / 255
                    for item in rgb:
                        screen_data[spos + item] = int(cursor_data[cpos + item] * alpha + screen_data[spos + item] * (1 - alpha))

        return screenshot

    @staticmethod
    def _cfactory(attr: Any, func: str, argtypes: List[Any], restype: Any, errcheck: Optional[Callable] = None):

        meth = getattr(attr, func)
        meth.argtypes = argtypes
        meth.restype = restype

        if errcheck:
            meth.errcheck = errcheck

    def _set_cfunctions(self) -> None:

        cfactory = self._cfactory
        attrs = {
            "gdi32": self.gdi32,
            "user32": self.user32,
        }

        for func, (attr, argtypes, restype) in CFUNCTIONS.items():
            cfactory(
                attr=attrs[attr],
                func=func,
                argtypes=argtypes,
                restype=restype,
            )

    def _set_dpi_awareness(self) -> None:

        version = getwindowsversion()[:2]

        if version >= (6, 3):
            windll.shcore.SetProcessDpiAwareness(2)

        elif (6, 0) <= version < (6, 3):
            self.user32.SetProcessDPIAware()

    def _get_srcdc(self) -> int:

        current_thread_index = current_thread()
        current_srcdc = Screencapture._srcdc_dict.get(current_thread_index) or Screencapture._srcdc_dict.get(main_thread())

        if current_srcdc:
            srcdc = current_srcdc

        else:
            srcdc = self.user32.GetWindowDC(0)
            Screencapture._srcdc_dict[current_thread_index] = srcdc

        return srcdc

    def _monitors_impl(self) -> None:

        int_ = int
        user32 = self.user32
        get_system_metrics = user32.GetSystemMetrics

        self._monitors.append(
            {
                "left": int_(get_system_metrics(76)),
                "top": int_(get_system_metrics(77)),
                "width": int_(get_system_metrics(78)),
                "height": int_(get_system_metrics(79)),
            }
        )

        def _callback(monitor: int, data: HDC, rect: LPRECT, dc_: LPARAM) -> int:

            rct = rect.contents
            self._monitors.append(
                {
                    "left": int_(rct.left),
                    "top": int_(rct.top),
                    "width": int_(rct.right) - int_(rct.left),
                    "height": int_(rct.bottom) - int_(rct.top),
                }
            )

            return 1

        callback = MONITORNUMPROC(_callback)
        user32.EnumDisplayMonitors(0, 0, callback, 0)

    def _grab_impl(self, monitor: Monitor) -> Screen:

        srcdc, memdc = self._get_srcdc(), Screencapture.memdc
        width, height = monitor["width"], monitor["height"]

        if (self._bbox["height"], self._bbox["width"]) != (height, width):

            self._bbox = monitor
            self._bmi.bmiHeader.biWidth = width
            self._bmi.bmiHeader.biHeight = -height
            self._data = create_string_buffer(width * height * 4)

            if Screencapture.bmp:
                self.gdi32.DeleteObject(Screencapture.bmp)

            Screencapture.bmp = self.gdi32.CreateCompatibleBitmap(srcdc, width, height)
            self.gdi32.SelectObject(memdc, Screencapture.bmp)

        self.gdi32.BitBlt(memdc, 0, 0, width, height, srcdc, monitor["left"], monitor["top"], SRCCOPY | CAPTUREBLT)
        bits = self.gdi32.GetDIBits(memdc, Screencapture.bmp, 0, height, self._data, self._bmi, DIB_RGB_COLORS)

        if bits != height:
            pass

        return self.cls_image(bytearray(self._data), monitor)

    def _cursor_impl(self) -> Optional[Screen]:
        return None

    def grab(self, monitor: Union[Monitor, Tuple[int, int, int, int]]):

        if isinstance(monitor, tuple):
            monitor = {
                "left": monitor[0],
                "top": monitor[1],
                "width": monitor[2] - monitor[0],
                "height": monitor[3] - monitor[1],
            }

        with lock:

            screenshot = self._grab_impl(monitor)
            if self.with_cursor:

                cursor = self._cursor_impl()
                screenshot = self._merge(screenshot, cursor)

            return screenshot

    def save_in_memory(self):

        monitors = [dict(monitor) for monitor in set(tuple(monitor.items()) for monitor in self.monitors)]

        for index, display in enumerate(monitors):
            sct = self.grab(display)
            output = self.create_png(sct.rgb, sct.size, level=self.compression_level, output=None)

            yield output

    def create_in_memory(self, **kwargs: Any):

        kwargs["monitor"] = kwargs.get("monitor", 1)
        return [image for image in self.save_in_memory()]

    @staticmethod
    def create_png(data: bytes, size: Tuple[int, int], level: int = 6, output: Optional[str] = None):

        width, height = size
        line = width * 3
        png_filter = pack(">B", 0)
        scanlines = b"".join([png_filter + data[y * line:y * line + line] for y in range(height)])
        magic = pack(">8B", 137, 80, 78, 71, 13, 10, 26, 10)

        ihdr = [b"", b"IHDR", b"", b""]
        ihdr[2] = pack(">2I5B", width, height, 8, 2, 0, 0, 0)
        ihdr[3] = pack(">I", crc32(b"".join(ihdr[1:3])) & 0xFFFFFFFF)
        ihdr[0] = pack(">I", len(ihdr[2]))

        idat = [b"", b"IDAT", compress(scanlines, level), b""]
        idat[3] = pack(">I", crc32(b"".join(idat[1:3])) & 0xFFFFFFFF)
        idat[0] = pack(">I", len(idat[2]))

        iend = [b"", b"IEND", b"", b""]
        iend[3] = pack(">I", crc32(iend[1]) & 0xFFFFFFFF)
        iend[0] = pack(">I", len(iend[2]))

        if not output:
            return magic + b"".join(ihdr + idat + iend)

        with open(output, "wb") as fileh:
            fileh.write(magic)
            fileh.write(b"".join(ihdr))
            fileh.write(b"".join(idat))
            fileh.write(b"".join(iend))

            fileh.flush()
            fsync(fileh.fileno())

        return None
