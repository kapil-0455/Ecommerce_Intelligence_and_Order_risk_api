import requests

def test_httpx_api():
    response = requests.post("http://localhost:8000/customer-order",
        json={
            "customer_id": 501,
            "order_id": 9001
        }
    )

    assert response.status_code == 200