from ctypes import windll

from helper.helpers.config import MessageConfig


class Message:
    """
    Shows a fake error window.
    """
    def __init__(self):

        self.__config = MessageConfig()

    def __create_message_window(self) -> None:
        """
        Creates a fake error window.

        Parameters:
        - None.

        Returns:
        - None.
        """
        windll.user32.MessageBoxW(0, self.__config.MessageDescription, self.__config.MessageTitle, 0x10)

    def run(self) -> None:
        """
        Launches the fake error window module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__create_message_window()

        except Exception as e:
            pass
