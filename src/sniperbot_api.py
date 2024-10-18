#  This file is part of SniperCallsBot (https://github.com/Drakkar-Software/SniperCallsBot)
#  Copyright (c) 2023 Drakkar-Software, All rights reserved.
#
#  SniperCallsBot is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  SniperCallsBot is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public
#  License along with SniperCallsBot. If not, see <https://www.gnu.org/licenses/>.
import src.constants as constants
import src.commands as commands
import SniperCallsbot_commons.constants as commons_constants
import src.automation as automation


class SniperCallsBotAPI:

    def __init__(self, SniperCallsbot):
        self._SniperCallsbot = SniperCallsbot

    def is_initialized(self) -> bool:
        return self._SniperCallsbot.initialized

    def get_exchange_manager_ids(self) -> list:
        return self._SniperCallsbot.exchange_producer.exchange_manager_ids

    def get_global_config(self) -> dict:
        return self._SniperCallsbot.config

    def get_startup_config(self, dict_only=True):
        return self._SniperCallsbot.get_startup_config(constants.CONFIG_KEY, dict_only=dict_only)

    def get_edited_config(self, dict_only=True):
        return self._SniperCallsbot.get_edited_config(constants.CONFIG_KEY, dict_only=dict_only)

    def get_startup_tentacles_config(self):
        return self._SniperCallsbot.get_startup_config(constants.TENTACLES_SETUP_CONFIG_KEY)

    def get_edited_tentacles_config(self):
        return self._SniperCallsbot.get_edited_config(constants.TENTACLES_SETUP_CONFIG_KEY)

    def set_edited_tentacles_config(self, config):
        self._SniperCallsbot.set_edited_config(constants.TENTACLES_SETUP_CONFIG_KEY, config)

    def get_trading_mode(self):
        return self._SniperCallsbot.get_trading_mode()

    def get_tentacles_setup_config(self):
        return self._SniperCallsbot.tentacles_setup_config

    def get_startup_messages(self) -> list:
        return self._SniperCallsbot.startup_messages

    def get_start_time(self) -> float:
        return self._SniperCallsbot.start_time

    def get_bot_id(self) -> str:
        return self._SniperCallsbot.bot_id

    def get_matrix_id(self) -> str:
        return self._SniperCallsbot.evaluator_producer.matrix_id

    def get_aiohttp_session(self) -> object:
        return self._SniperCallsbot.get_aiohttp_session()

    def get_automation(self) -> automation.Automation:
        return self._SniperCallsbot.automation

    def get_interface(self, interface_class):
        for interface in self._SniperCallsbot.interface_producer.interfaces:
            if isinstance(interface, interface_class):
                return interface

    def run_in_main_asyncio_loop(self, coroutine, log_exceptions=True,
                                 timeout=commons_constants.DEFAULT_FUTURE_TIMEOUT):
        return self._SniperCallsbot.run_in_main_asyncio_loop(coroutine, log_exceptions=log_exceptions, timeout=timeout)

    def run_in_async_executor(self, coroutine):
        return self._SniperCallsbot.task_manager.run_in_async_executor(coroutine)

    def stop_tasks(self) -> None:
        self._SniperCallsbot.task_manager.stop_tasks()

    def stop_bot(self) -> None:
        commands.stop_bot(self._SniperCallsbot)

    @staticmethod
    def restart_bot() -> None:
        commands.restart_bot()

    def update_bot(self) -> None:
        commands.update_bot(self)
