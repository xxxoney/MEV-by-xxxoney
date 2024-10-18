from os import path
from typing import List
from ctypes.wintypes import DWORD
from ctypes import windll, sizeof, byref, create_unicode_buffer

from helper.helpers.dataclasses import Data
from helper.helpers import functions, ProcessMemoryCountersEx, MemoryStorage


class Processes:
    """
    Collects all running processes.
    """
    def __init__(self, folder: str):

        self.__file = path.join(folder, "Processes.txt")
        self.__storage = MemoryStorage()

    @staticmethod
    def get_processes_list() -> List:

        process_list = []
        process_ids = (DWORD * 4096)()
        bytes_needed = DWORD()
        mb = (1024 * 1024)

        windll.psapi.EnumProcesses(byref(process_ids), sizeof(process_ids), byref(bytes_needed))

        for index in range(int(bytes_needed.value / sizeof(DWORD))):
            process_id = process_ids[index]

            try:

                process_handle = windll.kernel32.OpenProcess(0x0400 | 0x0010, False, process_id)
                memory_info = ProcessMemoryCountersEx()
                memory_info.cb = sizeof(ProcessMemoryCountersEx)

                if windll.psapi.GetProcessMemoryInfo(process_handle, byref(memory_info), sizeof(memory_info)):
                    process_name = create_unicode_buffer(512)
                    windll.psapi.GetModuleFileNameExW(process_handle, 0, process_name, sizeof(process_name))

                    process_list.append([
                        path.basename(process_name.value),
                        f"{memory_info.WorkingSetSize // mb} MB",
                        process_id
                    ])

                windll.kernel32.CloseHandle(process_handle)

            except:
                pass

        return process_list

    def __get_system_processes(self) -> None:
        """
        Collects all running processes.

        Parameters:
        - None.

        Returns:
        - None.
        """
        self.__storage.add_from_memory(
            self.__file,
            "\n".join(line for line in functions.create_table(["Name", "Memory", "PID"], self.get_processes_list()))
        )

    def run(self) -> Data:
        """
        Launches the processes collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_system_processes()

            return self.__storage.get_data()

        except Exception as e:
            pass
