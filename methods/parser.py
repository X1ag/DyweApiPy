import asyncio
from datetime import datetime, timedelta
import time
import json
import os
import threading
from methods.get_floor import get_nft_collection_floor

os.environ['TZ'] = 'Europe/Moscow'

prices = []
close_price = None
isClose = False
now = datetime.now()
close_time = (now + timedelta(minutes=5)).replace(minute=0, second=0, microsecond=0)
open_time = now.replace(second=0, microsecond=0)
prices = []  

def get_time():
    global open_time,close_time, prices
    # Обновление текущего времени
    now = datetime.now()
    if len(prices)> 0 and close_time <= now.replace(second=0, microsecond=0):
        filename='./candles/candlesANON.json'
        if os.path.exists(filename): 
            with open(filename, 'r+') as json_file:
                json_data = json.load(json_file)
        else:
            json_data = {"data": []}

        data = {
                    'openTime':int(open_time.timestamp() * 1000),
                    'closeTime':int(close_time.timestamp() * 1000),
                    'percentChangePrice': percentChange(),
                    'currentPrice': prices[-1],
                    'open': prices[0],
                    'high': max(prices),
                    'low': min(prices),
                    'close': prices[-1],
        }
        # Добавляем новые данные в список "data"
        json_data["data"].append(data)
        # Записываем обновленные данные в файл
        with open(filename, 'w+') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"File \033[96mcandlesANON\033[0m.json updated, request amount: {len(prices)}")
        prices.clear()
        close_time = (now + timedelta(minutes=5)).replace(second=0, microsecond=0)
        open_time = now.replace(second=0, microsecond=0)

    print(f'\033[92m close time: {close_time} \033[0m')
    return open_time, close_time

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

async def writeFloorInFile(data, address: str = "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N"):
    with open(f'./candles/candles{address}.json', 'w+', encoding='utf8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
                    print(f"File \033[96mcandles{address}\033[0m.json updated, request amount: {len(prices)}")
                    file.write('\n')
                    
async def getData(address: str = "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N"):
    while True:
        try:
            data = {
                'openTime': int(get_time()[0].timestamp() * 1000),
                'closeTime':int(get_time()[1].timestamp() * 1000),
                'percentChangePrice': percentChange(),
                'currentPrice': await getPrice(address),
                'open': prices[0],
                'high': max(prices),
                'low': min(prices),
                'close': prices[-1],
            }
            print(f'\033[93m Collected data: {data} \033[0m')
            if data:
                await writeFloorInFile(data, address)
        except Exception as e:
            print(f"Bro, eto oshibka bro: {e}")
        await asyncio.sleep(5)

async def main(address):
    time.tzset()
    print('Starting main function')
    await getData(address)

if __name__ == "__main__":
    address = "EQBcjALtmHwSBCSpDOZ1_emrSQVtJU6J0POZR-ThkZjfXkZs"
    asyncio.run(main(address))