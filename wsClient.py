import websocket

def on_open(ws):
	print('con opened')
	ws.send('Hello, server!')

def on_close(ws):
	print('con closed')

def on_message(ws, message):
	print('received: ' + message)

ws = websocket.WebSocketApp("ws://localhost:8765", on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()