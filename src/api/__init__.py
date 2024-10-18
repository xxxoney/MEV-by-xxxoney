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

from src.api import backtesting
from src.api import strategy_optimizer
from src.api import updater

from src.api.backtesting import (
    create_independent_backtesting,
    check_independent_backtesting_remaining_objects,
    is_independent_backtesting_in_progress,
    is_independent_backtesting_computing,
    get_independent_backtesting_progress,
    is_independent_backtesting_finished,
    is_independent_backtesting_stopped,
    get_independent_backtesting_exchange_manager_ids,
    get_independent_backtesting_bot_id,
    log_independent_backtesting_report,
    get_independent_backtesting_config,
    get_independent_backtesting_symbols_by_exchanges,
    initialize_and_run_independent_backtesting,
    join_independent_backtesting,
    initialize_independent_backtesting_config,
    clear_backtesting_fetched_data,
    stop_independent_backtesting,
    join_independent_backtesting_stop,
    get_independent_backtesting_report,
)
from src.api.strategy_optimizer import (
    create_strategy_optimizer,
    create_design_strategy_optimizer,
    find_optimal_configuration,
    initialize_design_strategy_optimizer,
    update_strategy_optimizer_total_runs,
    generate_and_save_strategy_optimizer_runs,
    create_strategy_optimizer_settings,
    resume_design_strategy_optimizer,
    cancel_strategy_optimizer,
    print_optimizer_report,
    get_optimizer_report,
    get_optimizer_results,
    get_optimizer_overall_progress,
    get_design_strategy_optimizer_queue,
    update_design_strategy_optimizer_queue,
    is_optimizer_in_progress,
    is_optimizer_computing,
    is_optimizer_finished,
    get_optimizer_errors_description,
    get_optimizer_current_test_suite_progress,
    get_optimizer_strategy,
    get_optimizer_all_time_frames,
    get_optimizer_all_TAs,
    get_optimizer_all_risks,
    get_optimizer_trading_mode,
    get_optimizer_is_properly_initialized,
)
from src.api.updater import (
    get_updater,
)

__all__ = [
    "create_independent_backtesting",
    "check_independent_backtesting_remaining_objects",
    "is_independent_backtesting_in_progress",
    "is_independent_backtesting_computing",
    "get_independent_backtesting_progress",
    "is_independent_backtesting_finished",
    "is_independent_backtesting_stopped",
    "get_independent_backtesting_exchange_manager_ids",
    "get_independent_backtesting_bot_id",
    "log_independent_backtesting_report",
    "get_independent_backtesting_config",
    "get_independent_backtesting_symbols_by_exchanges",
    "initialize_and_run_independent_backtesting",
    "join_independent_backtesting",
    "initialize_independent_backtesting_config",
    "clear_backtesting_fetched_data",
    "stop_independent_backtesting",
    "join_independent_backtesting_stop",
    "get_independent_backtesting_report",
    "create_strategy_optimizer",
    "create_design_strategy_optimizer",
    "find_optimal_configuration",
    "initialize_design_strategy_optimizer",
    "update_strategy_optimizer_total_runs",
    "generate_and_save_strategy_optimizer_runs",
    "create_strategy_optimizer_settings",
    "resume_design_strategy_optimizer",
    "cancel_strategy_optimizer",
    "print_optimizer_report",
    "get_optimizer_report",
    "get_optimizer_results",
    "get_optimizer_overall_progress",
    "get_design_strategy_optimizer_queue",
    "update_design_strategy_optimizer_queue",
    "is_optimizer_in_progress",
    "is_optimizer_computing",
    "is_optimizer_finished",
    "get_optimizer_errors_description",
    "get_optimizer_current_test_suite_progress",
    "get_optimizer_strategy",
    "get_optimizer_all_time_frames",
    "get_optimizer_all_TAs",
    "get_optimizer_all_risks",
    "get_optimizer_trading_mode",
    "get_optimizer_is_properly_initialized",
    "get_updater",
]
