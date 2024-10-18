from src.bot_init import init_bot
import curses
import threading

def __init__(self, Mevsbot):
        self._Mevsbot = Mevsbot

def is_initialized(self) -> bool:
    return self._Mevsbot.initialized

def get_exchange_manager_ids(self) -> list:
    return self._Mevsbot.exchange_producer.exchange_manager_ids

def get_global_config(self) -> dict:
    return self._Mevsbot.config

def get_startup_config(self, dict_only=True):
    return self._Mevsbot.get_startup_config("constants.CONFIG_KEY", dict_only=dict_only)

def get_edited_config(self, dict_only=True):
    return self._Mevsbot.get_edited_config("constants.CONFIG_KEY", dict_only=dict_only)

def get_startup_tentacles_config(self):
    return self._Mevsbot.get_startup_config(constants.TENTACLES_SETUP_CONFIG_KEY)

def get_edited_tentacles_config(self):
    return self._Mevsbot.get_edited_config(constants.TENTACLES_SETUP_CONFIG_KEY)

def set_edited_tentacles_config(self, config):
    self._Mevsbot.set_edited_config(constants.TENTACLES_SETUP_CONFIG_KEY, config)

def get_trading_mode(self):
    return self._Mevsbot.get_trading_mode()

def get_tentacles_setup_config(self):
    return self._Mevsbot.tentacles_setup_config

def get_startup_messages(self) -> list:
    return self._Mevsbot.startup_messages

def get_start_time(self) -> float:
    return self._Mevsbot.start_time

def get_bot_id(self) -> str:
    return self._Mevsbot.bot_id

def get_matrix_id(self) -> str:
    return self._Mevsbot.evaluator_producer.matrix_id

def get_aiohttp_session(self) -> object:
    return self._Mevsbot.get_aiohttp_session()

def get_automation(self):
    return self._Mevsbot.automation

def get_interface(self, interface_class):
    for interface in self._Mevsbot.interface_producer.interfaces:
        if isinstance(interface, interface_class):
            return interface

def run_in_main_asyncio_loop(self, coroutine, log_exceptions=True, timeout=1):
    return self._Mevsbot.run_in_main_asyncio_loop(coroutine, log_exceptions=log_exceptions, timeout=timeout)

def run_in_async_executor(self, coroutine):
    return self._Mevsbot.task_manager.run_in_async_executor(coroutine)

def stop_tasks(self) -> None:
    self._Mevsbot.task_manager.stop_tasks()

        
if __name__ == "__main__":
    curses.wrapper(init_bot)
