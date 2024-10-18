from ctypes.wintypes import DWORD, ULONG, CHAR, MAX_PATH, LONG, WORD
from ctypes import Structure, POINTER, c_char, c_ulong, c_size_t, c_wchar, c_uint32, c_ulonglong


class DataBlob(Structure):
    _fields_ = [
        ("cbData", DWORD),
        ("pbData", POINTER(c_char))
    ]


class ProcessEntry32(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("cntUsage", DWORD),
        ("th32ProcessID", DWORD),
        ("th32DefaultHeapID", POINTER(ULONG)),
        ("th32ModuleID", DWORD),
        ("cntThreads", DWORD),
        ("th32ParentProcessID", DWORD),
        ("pcPriClassBase", LONG),
        ("dwFlags", DWORD),
        ("szExeFile", CHAR * MAX_PATH)
    ]


class ProcessMemoryCountersEx(Structure):
    _fields_ = [
        ("cb", c_ulong),
        ("PageFaultCount", c_ulong),
        ("PeakWorkingSetSize", c_size_t),
        ("WorkingSetSize", c_size_t),
        ("QuotaPeakPagedPoolUsage", c_size_t),
        ("QuotaPagedPoolUsage", c_size_t),
        ("QuotaPeakNonPagedPoolUsage", c_size_t),
        ("QuotaNonPagedPoolUsage", c_size_t),
        ("PagefileUsage", c_size_t),
        ("PeakPagefileUsage", c_size_t),
        ("PrivateUsage", c_size_t)
    ]


class DisplayDevice(Structure):
    _fields_ = [
        ("cb", c_ulong),
        ("DeviceName", c_wchar * 32),
        ("DeviceString", c_wchar * 128),
        ("StateFlags", c_ulong),
        ("DeviceID", c_wchar * 128),
        ("DeviceKey", c_wchar * 128)
    ]


class MemoryStatusEx(Structure):
    _fields_ = [
        ('dwLength', c_uint32),
        ('dwMemoryLoad', c_uint32),
        ('ullTotalPhys', c_ulonglong),
        ('ullAvailPhys', c_ulonglong),
        ('ullTotalPageFile', c_ulonglong),
        ('ullAvailPageFile', c_ulonglong),
        ('ullTotalVirtual', c_ulonglong),
        ('ullAvailVirtual', c_ulonglong),
        ('sullAvailExtendedVirtual', c_ulonglong)
    ]


class UlargeInteger(Structure):
    _fields_ = [
        ("LowPart", c_ulong),
        ("HighPart", c_ulong)
    ]


class BitmapInfoHeader(Structure):
    _fields_ = [
        ("biSize", DWORD),
        ("biWidth", LONG),
        ("biHeight", LONG),
        ("biPlanes", WORD),
        ("biBitCount", WORD),
        ("biCompression", DWORD),
        ("biSizeImage", DWORD),
        ("biXPelsPerMeter", LONG),
        ("biYPelsPerMeter", LONG),
        ("biClrUsed", DWORD),
        ("biClrImportant", DWORD)
    ]


class BitmapInfo(Structure):
    _fields_ = [
        ("bmiHeader", BitmapInfoHeader),
        ("bmiColors", DWORD * 3)
    ]
