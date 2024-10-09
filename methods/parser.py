import asyncio
from datetime import datetime, timedelta
import pprint
import time
import json
import os
from methods.get_floor import get_nft_collection_floor
os.environ['TZ'] = 'Europe/Moscow'

prices = []
close_price = None
isClose = False
now = datetime.now()

def get_open_hour():
    open_hour = (now - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    print(f'\033[92m Open hour: {open_hour} \033[0m')
    return open_hour

def get_close_hour():
    close_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)      
    print(f'\033[92m Close hour: {close_hour} \033[0m')
    return close_hour

async def getPrice(address):
    print(f'Fetching price for address: {address}')
    result = await get_nft_collection_floor(address)
    prices.append(result)
    print(f'\033[92m Price fetched: {result} \033[0m')
    return result

def percentChange():
    if len(prices) < 2:
        return None
    return ((prices[-1] - prices[0])/(prices[0]+prices[-1] / 2)) * 100

async def getData(address: str = "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N"):
    while True:
        try:
            data = {
                'openTime': int(get_open_hour().timestamp() * 1000),
                'closeTime': int(get_close_hour().timestamp() * 1000),
                'percentChangePrice': percentChange(),
                'currentPrice': await getPrice(address),
                'open': prices[0],
                'high': max(prices),
                'low': min(prices),
                'close': prices[-1],
            }
            print(f'\033[93m Collected data: {data} \033[0m')
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(5)

async def main(address, timeframe):
    time.tzset()
    print('Starting main function')
    await getData(address, timeframe)

if __name__ == "__main__":
    address = "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N"
    timeframe = "1h"
    asyncio.run(main(address, timeframe))