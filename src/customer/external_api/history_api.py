from http.server import BaseHTTPRequestHandler,HTTPServer
import json

class historyAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/history/"):
            customer_id=self.path.split('/')[-1]
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()

            response={
                "customer_id":int(customer_id),
                "previous_orders":8
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404,"Not found")



server=HTTPServer(("localhost",8003),historyAPI)
print("server started for history api")
server.serve_forever()