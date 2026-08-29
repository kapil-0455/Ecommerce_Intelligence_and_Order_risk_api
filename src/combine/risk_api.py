import asyncio
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import httpx


async def call_product_api(client, product_ids):

    response = await client.post(
        "http://localhost:8000/products", json={"product_ids": product_ids}
    )

    response.raise_for_status()

    return response.json()


async def call_customer_api(client, customer_id, order_id):

    response = await client.post(
        "http://localhost:8004/customer-order",
        json={"customer_id": customer_id, "order_id": order_id},
    )

    response.raise_for_status()

    return response.json()


async def fetch_order_data(customer_id, order_id, product_ids):

    async with httpx.AsyncClient() as client:
        product_result, customer_result = await asyncio.gather(
            call_product_api(client, product_ids),
            call_customer_api(client, customer_id, order_id),
        )

        return product_result, customer_result


def calculate_risk(product_result, customer_result):

    risk_score = 0
    reasons = []

    # Customer check
    if customer_result.get("customer_status") == "active":
        reasons.append("Customer is active")

    else:
        risk_score += 40

        reasons.append("Customer is not active")

    # Product availability check
    products = product_result.get("products", [])

    if products and all(
        product.get("availability") == "in_stock" for product in products
    ):
        reasons.append("Product availability confirmed")

    else:
        risk_score += 30

        reasons.append("Product availability issue")

    # Order amount check
    order_amount = customer_result.get("order_amount", 0)

    if order_amount <= 50000:
        reasons.append("Order amount within threshold")

    else:
        risk_score += 30

        reasons.append("Order amount exceeds threshold")

    # Decision
    if risk_score < 30:
        decision = "APPROVED"

    elif risk_score < 60:
        decision = "REVIEW"

    else:
        decision = "REJECTED"

    return risk_score, decision, reasons


class RiskApi(BaseHTTPRequestHandler):
    def send_json(self, status_code, data):

        response = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_POST(self):

        if self.path != "/risk":
            self.send_json(404, {"error": "Not Found"})

            return
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        customer_id = data["customer_id"]
        order_id = data["order_id"]
        product_ids = data.get("product_ids", [])

        product_result, customer_result = asyncio.run(
            fetch_order_data(customer_id, order_id, product_ids)
        )

        risk_score, decision, reasons = calculate_risk(product_result, customer_result)

        self.send_json(
            200,
            {
                "customer_id": customer_id,
                "order_id": order_id,
                "products": len(product_result.get("products", [])),
                "risk_score": risk_score,
                "decision": decision,
                "reason": reasons,
            },
        )


server = HTTPServer(("localhost", 8005), RiskApi)

print("Risk API running on http://localhost:8005")

server.serve_forever()
