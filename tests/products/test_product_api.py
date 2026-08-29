import requests


def test_product_api():

    response = requests.post(
        "http://localhost:8000/products", json={"product_ids": [1, 2, 3]}
    )

    assert response.status_code == 200

    data = response.json()

    assert "products" in data
    assert len(data["products"]) == 3


def test_product_response_schema():

    response = requests.post(
        "http://localhost:8000/products", json={"product_ids": [1]}
    )

    data = response.json()

    product = data["products"][0]

    assert "id" in product
    assert "name" in product
    assert "category" in product
    assert "price" in product
    assert "rating" in product
    assert "availability" in product


def test_invalid_product_input():

    response = requests.post("http://localhost:8000/products", json={"product_ids": []})

    assert response.status_code == 200

    data = response.json()

    assert "products" in data
    assert data["products"] == []
