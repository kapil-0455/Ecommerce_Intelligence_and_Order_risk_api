import asyncio

import httpx

DEFAULT_TIMEOUT  = 10
async def fetch_product(product_id : int) -> dict:
    url = f"https://dummyjson.com/products/{product_id}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url , timeout= DEFAULT_TIMEOUT )
            response.raise_for_status()
            return response.json()

    except httpx.TimeoutException:
         return {"id": product_id, "error": "Request Timeout"}

    except httpx.HTTPStatusError as exc:
         return {"id": product_id, "error": str(exc)}

    except httpx.RequestError as exc:
         return {"id": product_id, "error": str(exc)}

async def fetch_products(product_ids : int) -> dict:

    tasks = [fetch_product(product_id) for product_id in product_ids]

    return await asyncio.gather(*tasks)