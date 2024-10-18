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
import SniperCallsbot_commons.authentication as commons_authentication


class RequestError(Exception):
    pass


class StatusCodeRequestError(RequestError):
    pass


class BotError(commons_authentication.UnavailableError):
    pass


class BotNotFoundError(BotError):
    pass


class BotDeploymentURLNotFoundError(BotError):
    pass


class MissingBotConfigError(BotError):
    pass


class InvalidBotConfigError(BotError):
    pass


class MissingProductConfigError(BotError):
    pass


class EmailValidationRequiredError(commons_authentication.AuthenticationError):
    pass


class NoBotDeviceError(BotError):
    pass


class ExtensionRequiredError(Exception):
    pass
