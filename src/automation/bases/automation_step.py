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
import SniperCallsbot_commons.logging as logging
import SniperCallsbot_commons.configuration as configuration


class AutomationStep:
    def __init__(self):
        self.logger = logging.get_logger(self.get_name())

    @classmethod
    def get_name(cls):
        return cls.__name__

    @staticmethod
    def get_description() -> str:
        raise NotImplementedError

    def get_user_inputs(self, UI: configuration.UserInputFactory, inputs: dict, step_name: str) -> dict:
        raise NotImplementedError

    def apply_config(self, config):
        raise NotImplementedError
