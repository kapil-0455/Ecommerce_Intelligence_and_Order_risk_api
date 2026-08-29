from http.server import BaseHTTPRequestHandler,HTTPServer
import json
class orderAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/order/'):
            
            
            order_id=int(self.path.split('/')[-1])
            with open("data.json", "r") as file:
                data = json.load(file)

            for order in data:

                if order["order_id"] == order_id:

                    response = {
                        "order_id": order["order_id"],
                        "amount": order["order_amount"],
                        "status": order["order_status"]
                    }
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            return
        else:
            self.send_error(404,"not found")

    
    

server=HTTPServer(("localhost",8002),orderAPI)
print("server started orderApi")
server.serve_forever()