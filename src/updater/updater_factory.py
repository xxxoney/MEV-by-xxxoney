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

import SniperCallsbot_commons.os_util as os_util
import SniperCallsbot_commons.enums as commons_enums

import src.updater.binary_updater as binary_updater
import src.updater.python_updater as python_updater


def create_updater():
    bot_type = os_util.get_SniperCallsbot_type()

    if bot_type == commons_enums.SniperCallsBotTypes.DOCKER.value:
        return None
    if bot_type == commons_enums.SniperCallsBotTypes.BINARY.value:
        return binary_updater.BinaryUpdater()
    if bot_type == commons_enums.SniperCallsBotTypes.PYTHON.value:
        return python_updater.PythonUpdater()
    return None
