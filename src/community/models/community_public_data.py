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
import dataclasses
import src.community.supabase_backend.enums as enums
import src.community.models.strategy_data as strategy_data


class CommunityPublicData:
    def __init__(self):
        self.products = _DataElement({}, False)

    def set_products(self, products):
        self.products.value = {product[enums.ProductKeys.ID.value]: product for product in products}
        self.products.fetched = True

    def get_product_slug(self, product_id):
        return self.products.value[product_id][enums.ProductKeys.SLUG.value]

    def get_strategies(self, strategy_categories) -> list[strategy_data.StrategyData]:
        return [
            strategy_data.StrategyData.from_dict(strategy_dict)
            for strategy_dict in self.products.value.values()
            if self._get_category_type(strategy_dict) in strategy_categories
        ]

    def _get_category_type(self, product: dict):
        category = product.get("category") or {}
        return category.get("type")

    def get_strategy(self, strategy_id: str) -> strategy_data.StrategyData:
        return strategy_data.StrategyData.from_dict(self.products.value[strategy_id])


@dataclasses.dataclass
class _DataElement:
    value: any
    fetched: bool
