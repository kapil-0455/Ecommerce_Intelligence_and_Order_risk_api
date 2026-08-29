import requests

DEFAULT_TIMEOUT = 10


def fetch_product(product_id: int) -> dict:

    url = f"https://dummyjson.com/products/{product_id}"

    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)

        response.raise_for_status()

        return response.json()

    except requests.Timeout:
        return {"id": product_id, "error": "Request Timeout"}

    except requests.HTTPError as exc:
        return {"id": product_id, "error": str(exc)}

    except requests.RequestException as exc:
        return {"id": product_id, "error": str(exc)}
