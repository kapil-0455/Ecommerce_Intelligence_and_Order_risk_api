from http.server import BaseHTTPRequestHandler,HTTPServer
import requests
import json

class requestClient(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path=='/customer-order':
            try:
                length=int(self.headers['Content-Length'])
                body=self.rfile.read(length)
                body=body.decode()
                data=json.loads(body)
                customer_id=data["customer_id"]
                response=requests.get(f"http://localhost:8001/customer/{customer_id}",timeout=5.0)
                customer_data=response.json()
                print(customer_data)

                self.send_response(200)
                self.send_header("content-type","application/json")
                self.end_headers()

                self.wfile.write(json.dumps(customer_data).encode())
            except requests.exceptions.Timeout:
                return {
                    "staus_code":504,
                    "error":"timeout error"
                }
            except requests.exceptions.RequestException:
                return{
                    "status_code":502,
                    "error":"request-error"
                }
        else:
            self.send_error(404,"Not found")



server=HTTPServer(("localhost",8000),requestClient)
print("Request client server started")
server.serve_forever()

