from collections import namedtuple
from typing import Any, Dict, Optional, Type


class Screen:

    Monitor = Dict[str, int]
    Size = namedtuple("Size", "width, height")
    Position = namedtuple("Position", "left, top")

    def __init__(self, data: bytearray, monitor: Monitor, size: Optional[Size] = None):

        self.__pixels = None
        self.__rgb = None
        self.raw = data
        self.position = Screen.Position(monitor["left"], monitor["top"])
        self.size = Screen.Size(monitor["width"], monitor["height"]) if size is None else size

    @property
    def __array_interface__(self) -> Dict[str, Any]:

        return {
            "version": 3,
            "shape": (self.height, self.width, 4),
            "typestr": "|u1",
            "data": self.raw,
        }

    @classmethod
    def from_size(cls: Type["ScreenShot"], data: bytearray, width: int, height: int):

        monitor = {"left": 0, "top": 0, "width": width, "height": height}
        return cls(data, monitor)

    @property
    def rgb(self):

        if not self.__rgb:

            rgb = bytearray(self.height * self.width * 3)
            raw = self.raw
            rgb[::3] = raw[2::4]
            rgb[1::3] = raw[1::4]
            rgb[2::3] = raw[::4]
            self.__rgb = bytes(rgb)

        return self.__rgb

    @property
    def bgra(self):
        return bytes(self.raw)

    @property
    def height(self):
        return self.size.height

    @property
    def width(self):
        return self.size.width

    @property
    def left(self):
        return self.position.left

    @property
    def top(self):
        return self.position.top

    @property
    def pixels(self):

        if not self.__pixels:

            rgb = zip(self.raw[2::4], self.raw[1::4], self.raw[::4])
            self.__pixels = list(zip(*[iter(rgb)] * self.width))

        return self.__pixels

    def pixel(self, x: int, y: int):

        try:
            return self.pixels[y][x]
        except:
            pass
