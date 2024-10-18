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
import SniperCallsbot_backtesting.api as backtesting_api

import SniperCallsbot_commons.enums as common_enums

import SniperCallsbot_services.api as service_api
import SniperCallsbot_services.interfaces as service_interfaces
import SniperCallsbot_services.managers as service_managers
import SniperCallsbot_services.SniperCallsbot_channel_consumer as service_channel_consumer

import SniperCallsbot_tentacles_manager.api as tentacles_manager_api

import src.channels as SniperCallsbot_channels
import src.constants as constants


class InterfaceProducer(SniperCallsbot_channels.SniperCallsBotChannelProducer):
    """Initializer class:
    - Initialize services, constants and tools
    """

    def __init__(self, channel, SniperCallsbot):
        super().__init__(channel)
        self.SniperCallsbot = SniperCallsbot

        self.interfaces = []
        self.notifiers = []
        self.to_create_notifiers_count = 0

    async def start(self):
        in_backtesting = backtesting_api.is_backtesting_enabled(self.SniperCallsbot.config)
        await self._create_interfaces(in_backtesting)
        await self._create_notifiers(in_backtesting)
        await self.start_interfaces()

    async def start_interfaces(self):
        to_start_interfaces = self.interfaces
        started_interfaces = await service_managers.start_interfaces(to_start_interfaces)
        if len(started_interfaces) != len(to_start_interfaces):
            missing_interfaces = [interface.get_name()
                                  for interface in to_start_interfaces
                                  if interface not in started_interfaces]
            self.logger.error(
                f"{', '.join(missing_interfaces)} interface{'s' if len(missing_interfaces) > 1 else ''} "
                f"did not start properly.")

    async def register_exchange(self, exchange_id):
        for to_notify_instance in self.interfaces + self.notifiers:
            await self._register_exchange(to_notify_instance, exchange_id)

    async def register_interface(self, instance):
        if instance is not None:
            self.interfaces.append(instance)
            await self._register_existing_exchanges(instance)

    async def register_notifier(self, instance):
        self.notifiers.append(instance)
        await self._register_existing_exchanges(instance)
        if len(self.notifiers) == self.to_create_notifiers_count:
            await service_api.process_pending_notifications()

    async def _register_existing_exchanges(self, instance):
        for exchange_id in self.SniperCallsbot.exchange_producer.exchange_manager_ids:
            await self._register_exchange(instance, exchange_id)

    async def _create_interfaces(self, in_backtesting):
        # do not overwrite data in case of inner bots init (backtesting)
        if service_interfaces.get_bot_api() is None:
            service_api.initialize_global_project_data(self.SniperCallsbot.SniperCallsbot_api,
                                                       constants.PROJECT_NAME,
                                                       constants.LONG_VERSION)
        interface_factory = service_api.create_interface_factory(self.SniperCallsbot.config)
        interface_list = interface_factory.get_available_interfaces()
        for interface_class in interface_list:
            await self._create_interface_if_relevant(interface_factory, interface_class, in_backtesting,
                                                     self.SniperCallsbot.get_edited_config(constants.CONFIG_KEY,
                                                                                    dict_only=False))

    async def _create_notifiers(self, in_backtesting):
        notifier_factory = service_api.create_notifier_factory(self.SniperCallsbot.config)
        notifier_list = notifier_factory.get_available_notifiers()
        for notifier_class in notifier_list:
            await self._create_notifier_class_if_relevant(notifier_factory, notifier_class, in_backtesting,
                                                          self.SniperCallsbot.get_edited_config(constants.CONFIG_KEY,
                                                                                         dict_only=False))

    async def _create_interface_if_relevant(self, interface_factory, interface_class,
                                            backtesting_enabled, edited_config):
        if self._is_interface_relevant(interface_class, backtesting_enabled):
            await self.send(bot_id=self.SniperCallsbot.bot_id,
                            subject=common_enums.SniperCallsBotChannelSubjects.CREATION.value,
                            action=service_channel_consumer.SniperCallsBotChannelServiceActions.INTERFACE.value,
                            data={
                                service_channel_consumer.SniperCallsBotChannelServiceDataKeys.EDITED_CONFIG.value: 
                                    edited_config,
                                service_channel_consumer.SniperCallsBotChannelServiceDataKeys.BACKTESTING_ENABLED.value:
                                    backtesting_enabled,
                                service_channel_consumer.SniperCallsBotChannelServiceDataKeys.CLASS.value: interface_class,
                                service_channel_consumer.SniperCallsBotChannelServiceDataKeys.FACTORY.value: interface_factory
                            })

    async def _create_notifier_class_if_relevant(self, notifier_factory, notifier_class,
                                                 backtesting_enabled, edited_config):
        if self._is_notifier_relevant(notifier_class, backtesting_enabled):
            await self.send(bot_id=self.SniperCallsbot.bot_id,
                            subject=common_enums.SniperCallsBotChannelSubjects.CREATION.value,
                            action=service_channel_consumer.SniperCallsBotChannelServiceActions.NOTIFICATION.value,
                            data={
                                service_channel_consumer.SniperCallsBotChannelServiceDataKeys.EDITED_CONFIG.value:
                                    edited_config,
                                service_channel_consumer.SniperCallsBotChannelServiceDataKeys.BACKTESTING_ENABLED.value:
                                    backtesting_enabled,
                                service_channel_consumer.SniperCallsBotChannelServiceDataKeys.CLASS.value: notifier_class,
                                service_channel_consumer.SniperCallsBotChannelServiceDataKeys.FACTORY.value: notifier_factory,
                                service_channel_consumer.SniperCallsBotChannelServiceDataKeys.EXECUTORS.value:
                                    self.SniperCallsbot.task_manager.executors
                            })
            self.to_create_notifiers_count += 1

    async def _register_exchange(self, to_notify_instance, exchange_id):
        await self.send(bot_id=self.SniperCallsbot.bot_id,
                        subject=common_enums.SniperCallsBotChannelSubjects.UPDATE.value,
                        action=service_channel_consumer.SniperCallsBotChannelServiceActions.EXCHANGE_REGISTRATION.value,
                        data={
                            service_channel_consumer.SniperCallsBotChannelServiceDataKeys.INSTANCE.value: to_notify_instance,
                            service_channel_consumer.SniperCallsBotChannelServiceDataKeys.EXCHANGE_ID.value: exchange_id,
                        })

    def _is_interface_relevant(self, interface_class, backtesting_enabled):
        return service_api.is_enabled(interface_class) and \
               tentacles_manager_api.is_tentacle_activated_in_tentacles_setup_config(
                   self.SniperCallsbot.tentacles_setup_config,
                   interface_class.get_name()) and \
               all(service.get_is_enabled(self.SniperCallsbot.config) for service in interface_class.REQUIRED_SERVICES) and \
               (not backtesting_enabled or (
                           backtesting_enabled and service_api.is_enabled_in_backtesting(interface_class)))

    def _is_notifier_relevant(self, notifier_class, backtesting_enabled):
        return service_api.is_enabled_in_config(notifier_class, self.SniperCallsbot.config) and \
               tentacles_manager_api.is_tentacle_activated_in_tentacles_setup_config(
                   self.SniperCallsbot.tentacles_setup_config,
                   notifier_class.get_name()) and \
               all(service.get_is_enabled(self.SniperCallsbot.config)
                   for service in notifier_class.REQUIRED_SERVICES) and \
               not backtesting_enabled

    async def stop(self):
        self.logger.debug("Stopping ...")
        await service_managers.stop_interfaces(self.interfaces)
        self.logger.debug("Stopped")
