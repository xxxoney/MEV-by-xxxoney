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
import SniperCallsbot_tentacles_manager.api as tentacles_manager_api
import src.constants as constants
import SniperCallsbot_commons.databases as databases
import SniperCallsbot_commons.logging as logging
import SniperCallsbot_commons.errors as commons_errors
import src.databases_util as databases_util


class Initializer:
    """Initializer class:
    - Initialize services, constants and tools
    """

    def __init__(self, SniperCallsbot):
        self.SniperCallsbot = SniperCallsbot

    async def create(self, init_bot_storage):
        # initialize tentacle configuration
        tentacles_config_path = self.SniperCallsbot.get_startup_config(constants.CONFIG_KEY, dict_only=False).\
            get_tentacles_config_path()
        self.SniperCallsbot.tentacles_setup_config = tentacles_manager_api.get_tentacles_setup_config(tentacles_config_path)

        if init_bot_storage:
            try:
                # init bot storage
                await databases.init_bot_storage(
                    self.SniperCallsbot.bot_id,
                    databases_util.get_run_databases_identifier(
                        self.SniperCallsbot.config,
                        self.SniperCallsbot.tentacles_setup_config
                    ),
                    True
                )
            except commons_errors.ConfigTradingError as err:
                # already logged as error, don't display it twice
                logging.get_logger(self.__class__.__name__).warning(f"Error when initializing bot storage: {err}")
            except Exception as err:
                logging.get_logger(self.__class__.__name__).exception(
                    err, True, f"Error when initializing bot storage: {err}"
                )

        # create SniperCallsBot channel
        await self.SniperCallsbot.global_consumer.initialize()
