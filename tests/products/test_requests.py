import requests

from src.product.requests_client import fetch_product


def test_valid_product_request():

    result = fetch_product(1)

    assert result["id"] == 1
    assert "title" in result
    assert "category" in result
    assert "price" in result
    assert "rating" in result


def test_invalid_product_request():

    result = fetch_product(999999)

    assert result["id"] == 999999
    assert "error" in result


def test_httperror():

    result = fetch_product(999999)

    assert result["id"] == 999999
    assert "error" in result


def test_timeout():

    try:
        response = requests.get("https://httpbin.org/delay/20", timeout=1)

        assert response.status_code == 200

    except requests.Timeout:
        assert True
