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
import SniperCallsbot_commons.enums as common_enums

import SniperCallsbot_backtesting.api as backtesting_api

import SniperCallsbot_evaluators.api as evaluator_api
import SniperCallsbot_evaluators.SniperCallsbot_channel_consumer as evaluator_channel_consumer

import src.channels as SniperCallsbot_channel
import src.logger as logger


class EvaluatorProducer(SniperCallsbot_channel.SniperCallsBotChannelProducer):
    """EvaluatorFactory class:
    - Create evaluators
    """

    def __init__(self, channel, SniperCallsbot):
        super().__init__(channel)
        self.SniperCallsbot = SniperCallsbot
        self.tentacles_setup_config = self.SniperCallsbot.tentacles_setup_config

        self.matrix_id = None

    async def start(self):
        await evaluator_api.initialize_evaluators(self.SniperCallsbot.config, self.tentacles_setup_config)
        self.matrix_id = evaluator_api.create_matrix()
        await evaluator_api.create_evaluator_channels(
            self.matrix_id, is_backtesting=backtesting_api.is_backtesting_enabled(self.SniperCallsbot.config)
        )
        await logger.init_evaluator_chan_logger(self.matrix_id)

    async def create_evaluators(self, exchange_configuration):
        await self.send(bot_id=self.SniperCallsbot.bot_id,
                        subject=common_enums.SniperCallsBotChannelSubjects.CREATION.value,
                        action=evaluator_channel_consumer.SniperCallsBotChannelEvaluatorActions.EVALUATOR.value,
                        data={
                            evaluator_channel_consumer.SniperCallsBotChannelEvaluatorDataKeys.TENTACLES_SETUP_CONFIG.value:
                                self.SniperCallsbot.tentacles_setup_config,
                            evaluator_channel_consumer.SniperCallsBotChannelEvaluatorDataKeys.MATRIX_ID.value:
                                self.SniperCallsbot.evaluator_producer.matrix_id,
                            evaluator_channel_consumer.SniperCallsBotChannelEvaluatorDataKeys.EXCHANGE_CONFIGURATION.value:
                                exchange_configuration
                        })

    async def stop(self):
        self.logger.debug("Stopping ...")
        await evaluator_api.stop_all_evaluator_channels(self.matrix_id)
        self.logger.debug("Stopped")
