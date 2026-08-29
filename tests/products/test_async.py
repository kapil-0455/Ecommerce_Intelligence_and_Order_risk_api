import asyncio

from src.product.httpx_client import fetch_products


def test_concurrent_request():

    product_ids = [1, 2, 3, 4, 5]

    results = asyncio.run(
        fetch_products(product_ids)
    )

    assert len(results) == 5

    assert results[0]["id"] == 1
    assert results[1]["id"] == 2
    assert results[2]["id"] == 3
    assert results[3]["id"] == 4
    assert results[4]["id"] == 5


def test_partial_fail():

    results = asyncio.run(
        fetch_products([1, 2, 999999])
    )

    assert len(results) == 3

    assert results[0]["id"] == 1
    assert results[1]["id"] == 2

    assert results[2]["id"] == 999999
    assert "error" in results[2]