from http.server import BaseHTTPRequestHandler, HTTPServer
import httpx
import asyncio
import json


async def fetch_data(customer_id, order_id):

    async with httpx.AsyncClient() as client:
        try:

            customer = client.get(f"http://localhost:8001/customer/{customer_id}",timeout=5.0)
            order = client.get(f"http://localhost:8002/order/{order_id}",timeout=5.0)
            history = client.get(f"http://localhost:8003/history/{customer_id}",timeout=5.0)

            customer_response, order_response, history_response = await asyncio.gather(
                customer,
                order,
                history
            )

            return [customer_response.json(),order_response.json(),history_response.json()]
            
        except httpx.TimeoutException:
            return {
                "status_code": 504,
                "error": "timeout error"
            }

        except httpx.HTTPError:
            return {
                "status_code": 502,
                "error": "request error"
            }


class HttpxClient(BaseHTTPRequestHandler):

    def do_POST(self):

        if self.path == "/customer-order":

            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length)
            data = json.loads(body)

            customer_id = data["customer_id"]
            order_id = data["order_id"]

            customer, order, history = asyncio.run(fetch_data(customer_id, order_id))
            

            response = {
                "customer_id": customer["customer_id"],
                "order_id": order["order_id"],
                "order_amount": order["amount"],
                "customer_status": customer["status"],
                "previous_orders": history["previous_orders"],
                "order_status": order["status"]
            }
            print(response)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404,"Not found")


server = HTTPServer(("localhost", 8000), HttpxClient)
print("HTTPX client server started")
server.serve_forever()