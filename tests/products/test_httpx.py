import asyncio

from src.product.httpx_client import fetch_product, fetch_products


def test_async_request():

    result = asyncio.run(fetch_product(1))

    assert result["id"] == 1
    assert "title" in result
    assert "category" in result
    assert "price" in result
    assert "rating" in result


def test_http_error():

    result = asyncio.run(fetch_product(999999))

    assert result["id"] == 999999
    assert "error" in result


def test_timeout():

    result = asyncio.run(fetch_product(999999))

    assert "id" in result


def test_multiple_async_requests():

    results = asyncio.run(fetch_products([1, 2, 3]))

    assert len(results) == 3

    assert results[0]["id"] == 1
    assert results[1]["id"] == 2
    assert results[2]["id"] == 3
