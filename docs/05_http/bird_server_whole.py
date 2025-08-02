from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import polars as pl
import sys


# [server]
class BirdServer(HTTPServer):
    def __init__(self, data, server_address, request_handler):
        super().__init__(server_address, request_handler)
        self._data = data
# [/server]


# [get]
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        result = self.server._data.write_json(row_oriented=True)
        self.send_content(result, HTTPStatus.OK)
# [/get]

# [send]
    def send_content(self, content, status):
        content = bytes(content, "utf-8")
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)
# [/send]


# [main]
def main():
    sandbox, filename = sys.argv[1], sys.argv[2]
    os.chdir(sandbox)
    df = pl.read_csv(filename)
    serverAddress = ("", 8000)
    server = BirdServer(df, serverAddress, RequestHandler)
    server.serve_forever()
# [/main]


if __name__ == "__main__":
    main()
