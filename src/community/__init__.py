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

from src.community import errors
from src.community.errors import (
    RequestError,
    StatusCodeRequestError,
    BotError,
    BotNotFoundError,
    NoBotDeviceError,
)
from src.community import models
from src.community.models import (
    CommunityUserAccount,
    CommunityFields,
    CommunityTentaclesPackage,
    CommunitySupports,
    CommunityDonation,
    StartupInfo,
    StrategyData,
)
from src.community.supabase_backend import (
    PostgresFunctions,
    SyncConfigurationStorage,
    ASyncConfigurationStorage,
    AuthenticatedAsyncSupabaseClient,
    CommunitySupabaseClient,
)

from src.community import community_analysis
from src.community import community_manager
from src.community import authentication
from src.community import graphql_requests
from src.community import feeds
from src.community import errors_upload

from src.community.community_analysis import (
    get_community_metrics,
    get_current_SniperCallsbots_stats,
    can_read_metrics,
)
from src.community.community_manager import (
    CommunityManager,
)
from src.community.authentication import (
    CommunityAuthentication,
)
from src.community.graphql_requests import (
    select_startup_info_query,
    select_bot_query,
    select_bots_query,
    create_bot_query,
    create_bot_device_query,
    update_bot_config_and_stats_query,
    select_subscribed_profiles_query,
    update_bot_trades_query,
    upsert_bot_trades_query,
    update_bot_portfolio_query,
    upsert_historical_bot_portfolio_query,
)
from src.community.feeds import (
    AbstractFeed,
    CommunityWSFeed,
    CommunityMQTTFeed,
    community_feed_factory,
)
from src.community.errors_upload import (
    register_error_uploader,
    Error,
    ErrorsUploader,
)
from src.community.identifiers_provider import (
    IdentifiersProvider,
)

__all__ = [
    "RequestError",
    "StatusCodeRequestError",
    "BotError",
    "BotNotFoundError",
    "NoBotDeviceError",
    "IdentifiersProvider",
    "CommunityUserAccount",
    "CommunityFields",
    "get_community_metrics",
    "get_current_SniperCallsbots_stats",
    "can_read_metrics",
    "CommunityManager",
    "CommunityAuthentication",
    "CommunityTentaclesPackage",
    "CommunitySupports",
    "CommunityDonation",
    "register_error_uploader",
    "Error",
    "ErrorsUploader",
    "StartupInfo",
    "StrategyData",
    "PostgresFunctions",
    "SyncConfigurationStorage",
    "ASyncConfigurationStorage",
    "AuthenticatedAsyncSupabaseClient",
    "CommunitySupabaseClient",
    "select_startup_info_query",
    "select_bot_query",
    "select_bots_query",
    "create_bot_query",
    "create_bot_device_query",
    "update_bot_config_and_stats_query",
    "select_subscribed_profiles_query",
    "update_bot_trades_query",
    "upsert_bot_trades_query",
    "update_bot_portfolio_query",
    "upsert_historical_bot_portfolio_query",
    "AbstractFeed",
    "CommunityWSFeed",
    "CommunityMQTTFeed",
    "community_feed_factory",
]
