from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path =="/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok\n")
            return
        
        if self.path =="/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"hello\n")
            return
        
        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()