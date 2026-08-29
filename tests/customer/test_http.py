import requests

def test_customer_api():
    response = requests.get("http://localhost:8001/customer/501")

    assert response.status_code == 200