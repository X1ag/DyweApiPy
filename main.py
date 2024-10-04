import asyncio
from threading import Thread
import parser 
import api

def start_parser(address, timeframe):
	asyncio.run(parser.main(address, timeframe))

def start_main(address, timeframe):
	asyncio.run(api.main(address, timeframe))
 
thread1 = Thread(target=start_parser, args=("EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N", "1h"), daemon=True)
thread1.start()
start_main('EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N', '1h')

print('script started')