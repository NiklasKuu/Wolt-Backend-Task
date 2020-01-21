import pytest

from api import app

@pytest.fixture
def client():
    return app.test_client()


def test_restaurant_search(client):
    """Check that restaurants are returned with a valid query string, latitude and longitude"""
    res = client.get("/restaurants/search?q=a&lat=60.17045&lon=24.93147")
    assert res.status_code == 200
    assert len(res.json) > 0

    res = client.get("/restaurants/search?q=nothing should be found&lat=60.17045&lon=24.93147")
    assert res.status_code == 200
    assert len(res.json) == 0

    res = client.get("/restaurants/search?q=Momotoko Citycenter&lat=60.17045&lon=24.93147")
    assert res.status_code == 200
    assert len(res.json) == 1        
    
def test_invalid_query_string(client):
    """Check that invalid query strings return 400 and the apropriate error string."""
    res = client.get("/restaurants/search?q=&lat=60.17045&lon=24.93147")
    correct_json_data = {
        "error": "Query string length is missing or is too short (minimum length is 1 character)"
    }
    assert res.status_code == 400
    assert res.json == correct_json_data

    res = client.get("http://127.0.0.1:5000/restaurants/search")
    assert res.status_code == 400
    assert res.json == correct_json_data

    res = client.get("http://127.0.0.1:5000/restaurants/search?lat=60.17045&lon=24.93147")
    assert res.status_code == 400
    assert res.json == correct_json_data

def test_invalid_latitude(client):
    """Check that invalid latitude return 400 and the apropriate error string."""
    res = client.get("/restaurants/search?q=sushi&lat=&lon=24.93147")
    correct_json_data = {
        "error": "Latitude coordinate is missing or is not a float."
    }
    assert res.status_code == 400
    assert res.json == correct_json_data

    res = client.get("/restaurants/search?q=sushi&lat=asd&lon=24.93147")
    assert res.status_code == 400
    assert res.json == correct_json_data

    res = client.get("/restaurants/search?q=sushi&lon=24.93147")
    assert res.status_code == 400
    assert res.json == correct_json_data

def test_invalid_longitude(client):
    """Check that invalid longitude return 400 and the apropriate error string."""
    res = client.get("/restaurants/search?q=sushi&lat=60.17045&lon=")
    correct_json_data = {
        "error": "Longitude coordinate is missing is not a float."
    }
    assert res.status_code == 400
    assert res.json == correct_json_data

    res = client.get("/restaurants/search?q=sushi&lat=60.17045&lon=asd")
    assert res.status_code == 400
    assert res.json == correct_json_data

    res = client.get("/restaurants/search?q=sushi&lat=60.17045")
    assert res.status_code == 400
    assert res.json == correct_json_data

def check_invalid_distance(client):
    """Check that restaurants with coordinates further than 3km are not shown"""
    res = client.get("http://127.0.0.1:5000/restaurants/search?q=sushi&lat=90&lon=135")
    assert res.status_code == 200
    assert len(res.json) < 1 
