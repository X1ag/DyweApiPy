import asyncio
from datetime import datetime
import json

from get_floor import get_nft_collection_floor


async def writeFloorInJson(address: str = "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N", timeframe: str = "1h"):
    while True:
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'floor': await get_nft_collection_floor(address)
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
        
def main(address, timeframe):
		loop = asyncio.get_event_loop()
		loop.create_task(writeFloorInJson(address,timeframe))
		loop.run_forever()
  

if __name__ == '__main__':
		main("EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N", "1h")