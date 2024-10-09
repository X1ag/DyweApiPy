import websockets
from asyncio import get_event_loop

async def handler(websocket,path):
	print("connected")
	message = await websocket.recv()
	print(f"message received {message}") 
	with open('candles/candlesEQBcjALtmHwSBCSpDOZ1_emrSQVtJU6J0POZR-ThkZjfXkZs.json', 'r') as f:
		data =f.read()
		await websocket.send(data)
		
	
start_server = websockets.serve(handler, "localhost", 8765)

get_event_loop().run_until_complete(start_server)
get_event_loop().run_forever()