import random
<<<<<<< HEAD
<<<<<<< HEAD
import time
from typing import Union
import asyncio

from loguru import logger


async def run_module(module, wallet_number, key, recipient: Union[str, None] = None, settings: dict = {}):
    try:
        await module(
            wallet_number, 
            key, 
            recipient, 
            from_token=settings.get('from_token'),
            to_token=settings.get('to_token'),
            min_amount=settings.get('min_amount'),
            max_amount=settings.get('max_amount'),
            slippage=settings.get('slippage'),
            all_amount=settings.get('all_amount'),
            min_percent=settings.get('min_percent'),
            max_percent=settings.get('max_percent'),
        )

    except Exception as e:
        logger.error(e)


def _async_run_module(module, wallet_number, key, recipient, settings):
    asyncio.run(run_module(module, wallet_number, key, recipient, settings))


def main(
        websites,
        wallets,
        website_settings, 
        wait_between_wallets_max=30,
        wait_between_wallets_min=20,
        wait_between_websites_max=20,
        wait_between_websites_min=5,
        wait_between_cycles_max=((12*60*60)+90),
        wait_between_cycles_min=((12*60*60)+5),      
        ):

    
    while True:
        # iterate through the wallets
        for _, wallet_key in enumerate(wallets, start=1):
            # website transactions to perform at each website
            # iterate through websites
            for tuple in zip(websites, website_settings):
                logger.info(f"Running module {tuple[0].__name__} with wallet {wallet_key}")
                _async_run_module(
                    tuple[0],
                    _,
                    wallet_key,
                    None,
                    tuple[1]
                )
            
                # wait between website actions
                random_wait = random.randint(wait_between_websites_min, wait_between_websites_max)
                logger.info(f"Waiting between websites for {random_wait} seconds")
                time.sleep(random_wait)
            
            # wait between wallets
            random_wait = random.randint(wait_between_wallets_min, wait_between_wallets_max)
            logger.info(f"Waiting between wallets for {random_wait} seconds")
            time.sleep(random_wait)

        # wait between cycles
        random_wait = random.randint(wait_between_cycles_min, wait_between_cycles_max)
        logger.info(f"Waiting between cycles for {random_wait} seconds")
        time.sleep(random_wait)
        
        # change all the settings
        logger.info(f"Switching from_token and to_token")
        for setting in website_settings:
            # ETH to USDC or back
            setting['from_token'], setting['to_token'] = setting['to_token'], setting['from_token']
=======
=======
>>>>>>> 30c15bba68552d47a53a5f7d4cd386cad749b944
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import questionary
from loguru import logger
from questionary import Choice

from config import ACCOUNTS
from settings import (
    RANDOM_WALLET,
    SLEEP_TO,
    SLEEP_FROM,
    QUANTITY_THREADS,
    THREAD_SLEEP_FROM,
    THREAD_SLEEP_TO, REMOVE_WALLET,
)
from modules_settings import *
from utils.helpers import remove_wallet
from utils.sleeping import sleep


def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("1) Make bridge to Base", bridge_base),
            Choice("2) Make bridge on Orbiter", bridge_orbiter),
            Choice("3) Wrap ETH", wrap_eth),
            Choice("4) Unwrap ETH", unwrap_eth),
            Choice("5) Swap on Uniswap", swap_uniswap),
            Choice("6) Swap on Pancake", swap_pancake),
            Choice("7) Swap on WooFi", swap_woofi),
            Choice("8) Swap on BaseSwap", swap_baseswap),
            Choice("9) Swap on AlienSwap", swap_alienswap),
            Choice("10) Swap on Maverick", swap_maverick),
            Choice("11) Swap on Odos", swap_odos),
            Choice("12) Swap on 1inch", swap_inch),
            Choice("13) Swap on OpenOcean", swap_openocean),
            Choice("14) Swap on XYSwap", swap_xyswap),
            Choice("15) Bungee Refuel", bungee_refuel),
            Choice("16) Stargate bridge", stargate_bridge),
            Choice("17) Deposit Aave", deposit_aave),
            Choice("18) Withdraw Aave", withdraw_aave),
            Choice("19) Deposit MoonWell", deposit_moonwell),
            Choice("20) Withdraw MoonWell", withdraw_moonwell),
            Choice("21) Deposit RocketSam", deposit_rocketsam),
            Choice("22) Withdraw RocketSam", withdraw_rocketsam),
            Choice("23) Mint NFT on MintFun", mint_mintfun),
            Choice("24) Mint and Bridge Zerius NFT", mint_zerius),
            Choice("25) Mint ZkStars NFT", mint_zkstars),
            Choice("26) Dmail sending mail", send_mail),
            Choice("27) Send message L2Telegraph", send_message),
            Choice("28) Mint and bridge NFT L2Telegraph", bridge_nft),
            Choice("29) Create portfolio on Ray", create_portfolio),
            Choice("30) Create gnosis safe", create_safe),
            Choice("31) Mint NFT on NFTS2ME", mint_nft),
            Choice("32) Swap tokens to ETH", swap_tokens),
            Choice("33) Use Multiswap", swap_multiswap),
            Choice("34) Use custom routes", custom_routes),
            Choice("35) Check transaction count", "tx_checker"),
            Choice("36) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
        print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")
        sys.exit()
    return result


def get_wallets():
    wallets = [
        {
            "id": _id,
            "key": key,
        } for _id, key in enumerate(ACCOUNTS, start=1)
    ]

    return wallets


async def run_module(module, account_id, key):
    try:
        await module(account_id, key)
    except Exception as e:
        logger.error(e)

    if REMOVE_WALLET:
        remove_wallet(key)

    await sleep(SLEEP_FROM, SLEEP_TO)


def _async_run_module(module, account_id, key):
    asyncio.run(run_module(module, account_id, key))


def main(module):
    wallets = get_wallets()

    if RANDOM_WALLET:
        random.shuffle(wallets)

    with ThreadPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        for _, account in enumerate(wallets, start=1):
            executor.submit(
                _async_run_module,
                module,
                account.get("id"),
                account.get("key"),
            )
            time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))


if __name__ == '__main__':
    print("❤️ Subscribe to me – https://t.me/sybilwave\n")

    logger.add("logging.log")

    module = get_module()
    if module == "tx_checker":
        get_tx_count()
    else:
        main(module)

    print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
    print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")
<<<<<<< HEAD
>>>>>>> 30c15bba68552d47a53a5f7d4cd386cad749b944
=======
>>>>>>> 30c15bba68552d47a53a5f7d4cd386cad749b944
