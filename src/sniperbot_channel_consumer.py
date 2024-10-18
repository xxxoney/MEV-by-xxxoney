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
import async_channel.channels as channel_instances
import async_channel.util as channel_creator

import SniperCallsbot_commons.enums as enums
import SniperCallsbot_commons.logging as logging

import SniperCallsbot_evaluators.SniperCallsbot_channel_consumer as evaluator_channel_consumer

import SniperCallsbot_services.SniperCallsbot_channel_consumer as service_channel_consumer

import SniperCallsbot_trading.api as trading_api
import SniperCallsbot_trading.SniperCallsbot_channel_consumer as trading_channel_consumer

import src.channels as SniperCallsbot_channel
import src.logger as logger


class SniperCallsBotChannelGlobalConsumer:

    def __init__(self, SniperCallsbot):
        self.SniperCallsbot = SniperCallsbot
        self.logger = logging.get_logger(self.__class__.__name__)

        # the list of SniperCallsbot channel consumers
        self.SniperCallsbot_channel_consumers = []

        # the SniperCallsBot Channel instance
        self.SniperCallsbot_channel = None

    async def initialize(self):
        # Creates SniperCallsBot Channel
        self.SniperCallsbot_channel: SniperCallsbot_channel.SniperCallsBotChannel = await channel_creator.create_channel_instance(
            SniperCallsbot_channel.SniperCallsBotChannel, channel_instances.set_chan_at_id,
            is_synchronized=True, bot_id=self.SniperCallsbot.bot_id)

        # Initialize global consumer
        self.SniperCallsbot_channel_consumers.append(
            await self.SniperCallsbot_channel.new_consumer(self.SniperCallsbot_channel_callback, bot_id=self.SniperCallsbot.bot_id))

        # Initialize trading consumer
        self.SniperCallsbot_channel_consumers.append(
            await self.SniperCallsbot_channel.new_consumer(
                trading_channel_consumer.SniperCallsbot_channel_callback,
                bot_id=self.SniperCallsbot.bot_id,
                action=[action.value for action in trading_channel_consumer.SniperCallsBotChannelTradingActions]
            ))

        # Initialize evaluator consumer
        self.SniperCallsbot_channel_consumers.append(
            await self.SniperCallsbot_channel.new_consumer(
                evaluator_channel_consumer.SniperCallsbot_channel_callback,
                bot_id=self.SniperCallsbot.bot_id,
                action=[action.value for action in evaluator_channel_consumer.SniperCallsBotChannelEvaluatorActions]
            ))

        # Initialize service consumer
        self.SniperCallsbot_channel_consumers.append(
            await self.SniperCallsbot_channel.new_consumer(
                service_channel_consumer.SniperCallsbot_channel_callback,
                bot_id=self.SniperCallsbot.bot_id,
                action=[action.value for action in service_channel_consumer.SniperCallsBotChannelServiceActions]
            ))

    async def SniperCallsbot_channel_callback(self, bot_id, subject, action, data) -> None:
        """
        SniperCallsBot channel consumer callback
        :param bot_id: the callback bot id
        :param subject: the callback subject
        :param action: the callback action
        :param data: the callback data
        """
        if subject == enums.SniperCallsBotChannelSubjects.NOTIFICATION.value:
            if action == trading_channel_consumer.SniperCallsBotChannelTradingActions.EXCHANGE.value:
                if trading_channel_consumer.SniperCallsBotChannelTradingDataKeys.EXCHANGE_ID.value in data:
                    exchange_id = data[trading_channel_consumer.SniperCallsBotChannelTradingDataKeys.EXCHANGE_ID.value]
                    self.SniperCallsbot.exchange_producer.register_created_exchange_id(exchange_id)
                    await logger.init_exchange_chan_logger(exchange_id)
                    exchange_configuration = trading_api.get_exchange_configuration_from_exchange_id(exchange_id)
                    await self.SniperCallsbot.evaluator_producer.create_evaluators(exchange_configuration)
                    # If an exchange is created before interface producer is done, it will be registered via
                    # self.SniperCallsbot.interface_producer directly on creation
                    await self.SniperCallsbot.interface_producer.register_exchange(exchange_id)
            elif action == evaluator_channel_consumer.SniperCallsBotChannelEvaluatorActions.EVALUATOR.value:
                if not self.SniperCallsbot.service_feed_producer.started:
                    # Start service feeds now that evaluators registered their feed requirements
                    await self.SniperCallsbot.service_feed_producer.start_feeds()
            elif action == service_channel_consumer.SniperCallsBotChannelServiceActions.INTERFACE.value:
                await self.SniperCallsbot.interface_producer.register_interface(
                    data[service_channel_consumer.SniperCallsBotChannelServiceDataKeys.INSTANCE.value])
            elif action == service_channel_consumer.SniperCallsBotChannelServiceActions.NOTIFICATION.value:
                await self.SniperCallsbot.interface_producer.register_notifier(
                    data[service_channel_consumer.SniperCallsBotChannelServiceDataKeys.INSTANCE.value])
            elif action == service_channel_consumer.SniperCallsBotChannelServiceActions.SERVICE_FEED.value:
                await self.SniperCallsbot.service_feed_producer.register_service_feed(
                    data[service_channel_consumer.SniperCallsBotChannelServiceDataKeys.INSTANCE.value])

    async def stop(self) -> None:
        """
        Remove all SniperCallsBot Channel consumers
        """
        for consumer in self.SniperCallsbot_channel_consumers:
            await self.SniperCallsbot_channel.remove_consumer(consumer)
