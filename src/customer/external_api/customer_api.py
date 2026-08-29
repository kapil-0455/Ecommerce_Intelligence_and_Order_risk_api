from http.server import BaseHTTPRequestHandler,HTTPServer
import json
class customerAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/customer/"):
            customer_id=int(self.path.split("/")[-1])
            with open("data.json","r") as file:
                data=json.load(file)
            for customer in data:
                if customer["customer_id"]==customer_id:
                    response={
                "customer_id":customer["customer_id"],
                "status":customer["customer_status"]
            }
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            return
        else:
            self.send_error(404,"Not found")

server=HTTPServer(("localhost",8001),customerAPI)
print("server started for customer api")
server.serve_forever()