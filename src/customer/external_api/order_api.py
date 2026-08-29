from http.server import BaseHTTPRequestHandler,HTTPServer
import json
class orderAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/order/'):
            
            
            order_id=self.path.split('/')[-1]
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            response={
                "order_id":int(order_id),
                "amount":45000,
                "status":"processing"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404,"not found")

    
    

server=HTTPServer(("localhost",8002),orderAPI)
print("server started orderApi")
server.serve_forever()