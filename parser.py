import asyncio
from datetime import datetime, timedelta
import time
import json
import os
# import logging
from get_floor import get_nft_collection_floor
# import colorlog
os.environ['TZ'] = 'Europe/Moscow'
# console_formatter = colorlog.ColoredFormatter(
#     "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     log_colors={
#         'DEBUG': 'cyan',
#         'INFO': 'green',
#         'WARNING': 'yellow',
#         'ERROR': 'red',
#         'CRITICAL': 'bold_red',
#     }
# )

# # Создайте форматтер для логирования в файл (без цвета)
# file_formatter = logging.Formatter(
#     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )

# # Создайте обработчики для файла и консоли
# file_handler = logging.FileHandler("app.log")
# file_handler.setFormatter(file_formatter)

# console_handler = logging.StreamHandler()
# console_handler.setFormatter(console_formatter)

# # Настройте базовую конфигурацию логгера
# logging.basicConfig(level=logging.DEBUG,  # Уровень логирования
#                     handlers=[file_handler, console_handler])

# log = logging.getLogger(__name__)
prices = []
close_price = None
isClose = False

def get_seconds_until_next_hour():
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    print(f'Next hour: {next_hour.strftime("%Y-%m-%d %H:%M:%S")}')
    return (next_hour - now).total_seconds()

async def clear_prices_at_start_of_hour():
    global isClose, close_price  # добавляем close_price к глобальным переменным

    while True:
        seconds_until_next_hour = get_seconds_until_next_hour()
        print(f'Waiting for {seconds_until_next_hour} seconds')
        await asyncio.sleep(seconds_until_next_hour)

        print(f'Last price is: {prices[-1]}')
        isClose = True
        prices.clear()
        print('Prices cleared')
        
        print(f'Prices cleared at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        await asyncio.sleep(3600)
        
async def getPrice(address):
    print(f'Fetching price for address: {address}')
    result = await get_nft_collection_floor(address)
    prices.append(result)
    print(f'\033[92m Price fetched: {result} \033[0m')
    return result

async def calculateOpenPrice():
    open_price = prices[0] if prices else None
    print(f'\033[92m Open price: {open_price} \033[0m')
    return open_price

async def calculateHighPrice():
    high_price = max(prices) if prices else None
    print(f'\033[92m High price: {high_price} \033[0m')
    return high_price

async def calculateLowPrice():
    low_price = min(prices) if prices else None
    print(f'\033[92m Low price: {low_price} \033[0m')
    return low_price

async def calculateLastPrice(address):
    global isClose
    close_price = None
    if close_price is None and isClose:
        close_price = await get_nft_collection_floor(address)
        isClose = False
    print(f'\033[92m Close price: {close_price} \033[0m')
    return close_price 

async def writeFloorInFile(data, address: str = "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N", timeframe: str = "1h"):
    file_content = ''
    try:
        with open(f'candles/candles{address}{timeframe}.json', 'r', encoding='utf8') as file:
         file_content = file.read()
         if file_content.strip() == '':
                file_content = '[]'
    except FileNotFoundError:
            file_content = '[]'
    json_array = json.loads(file_content)
    json_array.append(data)

    with open(f'candles/candles{address}{timeframe}.json', 'w', encoding='utf8') as file:
                    json.dump(json_array, file, ensure_ascii=False, indent=2)
                    print(f"File \033[96mcandles{address}{timeframe}\033[0m.json updated, request amount: {len(prices)}")
                    file.write('\n')


async def getDataAndWrite(address: str = "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N", timeframe: str = "1h"):
    while True:
        try:
            data = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'price': await getPrice(address),
                'open': await calculateOpenPrice(),
                'high': await calculateHighPrice(),
                'low': await calculateLowPrice(),
                'close': await calculateLastPrice(address)
            }
            print(f'\033[93m Collected data: {data} \033[0m')
            if data:
                await writeFloorInFile(data, address, timeframe)
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(5)

async def main(address, timeframe):
    time.tzset()
    print('Starting main function')
    asyncio.create_task(clear_prices_at_start_of_hour())
    await getDataAndWrite(address, timeframe)

if __name__ == "__main__":
    address = "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N"
    timeframe = "1h"
    asyncio.run(main(address, timeframe))