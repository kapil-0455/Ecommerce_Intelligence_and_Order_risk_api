import asyncio
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.product.httpx_client import fetch_products


class ProductAPI(BaseHTTPRequestHandler):
    def send_json(self, status_code, data):

        response = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    def do_POST(self):

        if self.path != "/products":
            self.send_json(404, {"error": "Not Found"})
            return

        content_length = int(self.headers["Content-Length"], 0)

        body = self.rfile.read(content_length)

        data = json.loads(body)

        product_ids = data.get("product_ids", [])
        products = asyncio.run(fetch_products(product_ids))

        normalized_products = []
        for product in products:
            if "error" in product:
                normalized_products.append(product)
                
            normalized_products.append(
                {
                    "id": product["id"],
                    "name": product["title"],
                    "category": product["category"],
                    "price": product["price"],
                    "rating": product["rating"],
                    "availability": ("in_stock" if product["stock"] > 0 else "out_of_stock"),
                }
            )

        self.send_json(200, {"products": normalized_products})


server = HTTPServer(("localhost", 8000), ProductAPI)

print("api running on http://localhost:8000")

server.serve_forever()



