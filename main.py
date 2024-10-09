import asyncio
from threading import Thread

import uvicorn
import methods.parser as parser 
import methods.api as api

def start_parser(address, timeframe):
	asyncio.run(parser.main(address, timeframe))

def start_main():
	asyncio.run(api.main())
 
thread1 = Thread(target=start_parser, args=("EQBcjALtmHwSBCSpDOZ1_emrSQVtJU6J0POZR-ThkZjfXkZs", "1h"), daemon=True)
thread1.start()
start_main()
print('script started')