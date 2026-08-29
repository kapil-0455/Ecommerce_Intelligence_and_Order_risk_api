import requests
def test_response_schema():

    response = requests.post("http://localhost:8004/customer-order",
        json={
            "customer_id": 501,
            "order_id": 9001
        }
    )

    data = response.json()

    assert "customer_id" in data
    assert "order_id" in data
    assert "order_amount" in data
    assert "customer_status" in data
    assert "previous_orders" in data
    assert "order_status" in data