import http.server
import socketserver

PORT = 8000
DIRECTORY = "web"


class Handler (http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.server_forever()
    
    
    