from datetime import datetime 
from get_floor import get_nft_collection_floor
from quart import Quart, jsonify, request

app = Quart(__name__)

# Пример маршрута для GET-запроса
@app.route('/dyweapi/v1/getFloor/<address>', methods=['GET'])
async def get_resource(address):
    data = {
        'timestamp': datetime.now(),
        'floor': await get_nft_collection_floor(address)
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

