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
import asyncio

import SniperCallsbot_commons.enums as common_enums
import SniperCallsbot_commons.constants as common_constants

import SniperCallsbot_trading.api as trading_api
import SniperCallsbot_trading.SniperCallsbot_channel_consumer as trading_channel_consumer

import src.channels as SniperCallsbot_channel


class ExchangeProducer(SniperCallsbot_channel.SniperCallsBotChannelProducer):
    def __init__(self, channel, SniperCallsbot, backtesting, ignore_config=False):
        super().__init__(channel)
        self.SniperCallsbot = SniperCallsbot
        self.ignore_config = ignore_config

        self.backtesting = backtesting
        self.exchange_manager_ids = []

        self.to_create_exchanges_count = 0
        self.created_all_exchanges = asyncio.Event()

    async def start(self):
        self.to_create_exchanges_count = 0
        self.created_all_exchanges.clear()
        for exchange_name in trading_api.get_enabled_exchanges_names(self.SniperCallsbot.config):
            await self.create_exchange(exchange_name, self.backtesting)
            self.to_create_exchanges_count += 1

    def register_created_exchange_id(self, exchange_id):
        self.exchange_manager_ids.append(exchange_id)
        if len(self.exchange_manager_ids) == self.to_create_exchanges_count:
            self.created_all_exchanges.set()
            self.logger.debug(f"Exchange(s) created")

    async def stop(self):
        self.logger.debug("Stopping ...")
        for exchange_manager in trading_api.get_exchange_managers_from_exchange_ids(self.exchange_manager_ids):
            await trading_api.stop_exchange(exchange_manager)
        self.logger.debug("Stopped")

    async def create_exchange(self, exchange_name, backtesting):
        await self.send(bot_id=self.SniperCallsbot.bot_id,
                        subject=common_enums.SniperCallsBotChannelSubjects.CREATION.value,
                        action=trading_channel_consumer.SniperCallsBotChannelTradingActions.EXCHANGE.value,
                        data={
                            trading_channel_consumer.SniperCallsBotChannelTradingDataKeys.TENTACLES_SETUP_CONFIG.value:
                                self.SniperCallsbot.tentacles_setup_config,
                            trading_channel_consumer.SniperCallsBotChannelTradingDataKeys.MATRIX_ID.value:
                                self.SniperCallsbot.evaluator_producer.matrix_id,
                            trading_channel_consumer.SniperCallsBotChannelTradingDataKeys.BACKTESTING.value: backtesting,
                            trading_channel_consumer.SniperCallsBotChannelTradingDataKeys.EXCHANGE_CONFIG.value:
                                self.SniperCallsbot.config,
                            trading_channel_consumer.SniperCallsBotChannelTradingDataKeys.EXCHANGE_NAME.value: exchange_name,
                        })
