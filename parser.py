import asyncio
from datetime import datetime, timedelta
import time
import json
import os
from get_floor import get_nft_collection_floor
os.environ['TZ'] = 'Europe/Moscow'

prices = []
close_price = None

def get_seconds_until_next_hour():
  now = datetime.now()
  next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
  print(next_hour)
  return (next_hour - now).total_seconds()

async def clear_prices_at_start_of_hour():
  global close_price
  while True:
    seconds_until_next_hour = get_seconds_until_next_hour()
    await asyncio.sleep(seconds_until_next_hour)
    close_price = prices[-1]
    prices.clear()
    print(f'Prices cleared at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    await asyncio.sleep(3600)

async def getPrice(address):
  result = await get_nft_collection_floor(address)	
  prices.append(result)
  if result:
    return result
  return None

async def calculateOpenPrice():
  return prices[0]	

async def calculateHighPrice():
  return max(prices)	

async def calculateLowPrice():
  return min(prices)	

async def calculateLastPrice():
  return close_price 

async def writeFloorInJson(address: str = "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N", timeframe: str = "1h"):
    while True:
        try:
            data = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'price': await getPrice(address),
                'open': await calculateOpenPrice(),
                'high': await calculateHighPrice(),
                'low': await calculateLowPrice(),
                'close': await calculateLastPrice()
            }
            if data:
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
                    print(f"File candles{address}{timeframe}.json updated")
                    file.write('\n')

        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(5) 	

async def main(address, timeframe):
    time.tzset()
    asyncio.create_task(clear_prices_at_start_of_hour())
    await writeFloorInJson(address, timeframe)

if __name__ == '__main__':
    asyncio.run(main("EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N", "1h"))