from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import pandas as pd
import sys
from urllib.parse import urlparse, parse_qs


class BirdServer(HTTPServer):
    def __init__(self, data, server_address, request_handler):
        super().__init__(server_address, request_handler)
        self._data = data


class RequestHandler(BaseHTTPRequestHandler):
    # [get]
    def do_GET(self):
        result = self.filter_data()
        as_json = result.to_json(orient="records")
        self.send_content(as_json, HTTPStatus.OK)
    # [/get]

    # [filter]
    def filter_data(self):
        params = parse_qs(urlparse(self.path).query)
        result = self.server._data
        if "species" in params:
            species = params["species"][0]
            result = result[result["species_id"] == species]
        if "year" in params:
            year = int(params["year"][0])
            result = result[result["year"] == year]
        return result
    # [/filter]

    def send_content(self, content, status):
        content = bytes(content, "utf-8")
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main():
    sandbox, filename = sys.argv[1], sys.argv[2]
    os.chdir(sandbox)
    df = pd.read_csv(filename)
    serverAddress = ("", 8000)
    server = BirdServer(df, serverAddress, RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
