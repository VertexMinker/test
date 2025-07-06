from fastapi.testclient import TestClient
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from inventory_app.main import app

client = TestClient(app)


def test_list_items():
    res = client.get('/items')
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_forecast_no_history():
    # Should return 404 if no history
    items = client.get('/items').json()
    if items:
        item_id = items[0]['id']
        res = client.get(f'/forecast/{item_id}')
        assert res.status_code == 404
