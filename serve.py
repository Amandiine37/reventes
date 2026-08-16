import http.server
import socketserver
import os
import functools

PORT = 4173
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        if path == "/" or path.endswith(".html"):
            return "text/html; charset=utf-8"
        return super().guess_type(path)

Handler = functools.partial(Handler, directory=DIRECTORY)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
