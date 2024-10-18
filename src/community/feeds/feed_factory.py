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
import src.enums
import src.constants
import src.community.feeds.community_ws_feed as community_ws_feed
import src.community.feeds.community_mqtt_feed as community_mqtt_feed
import src.community.feeds.community_supabase_feed as community_supabase_feed


def community_feed_factory(authenticator, feed_type: src.enums.CommunityFeedType):
    feed_url = src.constants.COMMUNITY_FEED_URL
    if feed_type is src.enums.CommunityFeedType.WebsocketFeed:
        return community_ws_feed.CommunityWSFeed(feed_url, authenticator)
    if feed_type is src.enums.CommunityFeedType.MQTTFeed:
        return community_mqtt_feed.CommunityMQTTFeed(feed_url, authenticator)
    if feed_type is src.enums.CommunityFeedType.SupabaseFeed:
        return community_supabase_feed.CommunitySupabaseFeed(feed_url, authenticator)
    raise NotImplementedError(f"Unsupported feed type: {feed_type}")
