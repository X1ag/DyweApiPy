import pytest
import sys
sys.path.insert(0, '/home/x1ag/Projects/GetFloorPy/methods')
from api import app


@pytest.mark.asyncio
async def test_health():
	response = await app.test_client.get('/health')
	assert response.status == 200
	assert response.text == 'Health check: OK \n'