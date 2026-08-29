import requests

def test_not_found():
    response = requests.get("http://localhost:8001/wrong")

    assert response.status_code == 404