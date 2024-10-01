from datetime import datetime
import json
from quart import Quart, jsonify

app = Quart(__name__)

# Пример маршрута для GET-запроса
@app.route('/dyweapi/v1/getData/<address>/<timeframe>', methods=['GET'])
async def get_data(address, timeframe):
   try:
       with open(f'candles/candles{address}{timeframe}.json', 'r') as f:
            data = json.load(f)
            return jsonify(data)
   except FileNotFoundError:
       return jsonify({"error": "File not found"}), 404
   except json.decoder.JSONDecodeError:
       return jsonify({"error": "invalid Json"}), 404

if __name__ == '__main__':
    app.run(debug=True)