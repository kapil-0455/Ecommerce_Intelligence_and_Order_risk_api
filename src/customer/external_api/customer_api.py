from http.server import BaseHTTPRequestHandler,HTTPServer
import json
class customerAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/customer/"):
            customer_id=self.path.split("/")[-1]
            
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            response={
                "customer_id":int(customer_id),
                "status":"active"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404,"Not found")

server=HTTPServer(("localhost",8001),customerAPI)
print("server started for customer api")
server.serve_forever()