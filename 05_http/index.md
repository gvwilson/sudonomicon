# HTTP

## Start with Something Simple

```{data-file="get_remote.py"}
import requests

url = "https://gvwilson.github.io/sudonomicon/site/motto.txt"
response = requests.get(url)
print(f"status code: {response.status_code}")
print(f"body:\n{response.text}")
```
```{data-file="get_remote.out"}
status code: 200
body:
Start where you are, use what you have, help who you can.

```

-   Use the [`requests`][requests] module to send an [HTTP](g:http) [request](g:http_request)
-   The URL identifies the file we want
    -   Though as we'll see, the server can interpret it differently
-   Response includes:
    -   [HTTP status code](g:http_status_code) such as 200 (OK) or 404 (Not Found)
    -   The text of the response

## What Just Happened

-   Figure shows what happened

<figure id="http_lifecycle">
  <img src="http_lifecycle.svg" alt="HTTP request/response lifecycle"/>
  <figcaption>Figure 1: Lifecycle of an HTTP request and response</figcaption>
</figure>

-   Open a connection to the server
-   Send an [HTTP request](g:http_request) for the file we want
-   Server creates a [response](g:http_response) that includes the contents of the file
-   Sends it back
-   `requests` parses the response and creates a Python object for us

## Request Structure

```{data-file="dump_structure.py"}
import requests
from requests_toolbelt.utils import dump

url = "https://gvwilson.github.io/sudonomicon/site/motto.txt"
response = requests.get(url)
data = dump.dump_all(response)
print(str(data, "utf-8"))
```
```{data-file="dump_structure.out"}
GET /safety-tutorial/site/motto.txt HTTP/1.1
Host: gvwilson.github.io
User-Agent: python-requests/2.31.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive

```

-   First line is [method](g:http_method), URL, and protocol version
-   Every HTTP request can have [headers](g:http_header) with extra information
    -   And optionally data being uploaded
-   Yes, it's all just text
    -   Except for uploaded data, which is just bytes

## Response Structure

```{data-file="response_headers.py"}
import requests

url = "https://gvwilson.github.io/sudonomicon/site/motto.txt"
response = requests.get(url)
for key, value in response.headers.items():
    print(f"{key}: {value}")
```
```{data-file="response_headers.out"}
Connection: keep-alive
Content-Length: 5142
Server: GitHub.com
Content-Type: text/html; charset=utf-8
permissions-policy: interest-cohort=()
ETag: W/"65c56fc7-239b"
Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; img-src data:; connect-src 'self'
Content-Encoding: gzip
X-GitHub-Request-Id: A08C:5A357:7CF794:9CEA06:65D13923
Accept-Ranges: bytes
Date: Sat, 17 Feb 2024 22:54:27 GMT
Via: 1.1 varnish
Age: 0
X-Served-By: cache-yyz4563-YYZ
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1708210467.301651,VS0,VE20
Vary: Accept-Encoding
X-Fastly-Request-ID: cb16df2dfa73aaf6de87924c743dd1e50a0ce570
```

-   Every HTTP response also has with extra information
    -   Does *not* include status code: that appears in the first line
-   Most important for now are:
    -   `Content-Length`: number of bytes in response data (i.e., how much to read)
    -   `Content-Type`: [MIME type](g:mime_type) of data (e.g., `text/plain`)
-   From now on we will only show interesting headers

## Exercise {: .exercise}

1.  Add header called `Studying` with the value `safety`
    to the `requests` script shown above.
    Does it make a difference to the response?
    Should it?

1.  What is the difference between the `Content-Type` and the `Content-Encoding` headers?

## When Things Go Wrong

```{data-file="get_404.py"}
import requests

url = "https://gvwilson.github.io/sudonomicon/site/nonexistent.txt"
response = requests.get(url)
print(f"status code: {response.status_code}")
print(f"body length: {len(response.text)}")
```
```{data-file="get_404.out"}
status code: 404
body length: 9115
```

-   The 404 status code tells us something went wrong
-   The 9 kilobyte response is an HTML page with an embedded image (the GitHub logo)
-   The page contains human-readable error messages
    -   But we have to know page format to pull them out

## Exercise {: .exercise}

Look at [this list of HTTP status codes][http_status_codes].

1.  What is the difference between status code 403 and status code 404?

2.  What is status code 418 used for?

3.  Under what circumstances would you expect to get a response whose status code is 505?

## Getting JSON

```{data-file="get_json.py"}
import requests

url = "https://gvwilson.github.io/sudonomicon/site/motto.json"
response = requests.get(url)
print(f"status code: {response.status_code}")
print(f"body as text: {len(response.text)} bytes")
as_json = response.json()
print(f"body as JSON:\n{as_json}")
```
```{data-file="get_json.out"}
status code: 200
body as text: 107 bytes
body as JSON:
{'first': 'Start where you are', 'second': 'Use what you have', 'third': 'Help who you can'}
```

-   Parsing data out of HTML is called [web scraping](g:web_scraping)
    -   Painful and error prone
-   Better to have the server return data as data
    -   Preferred format these days is [JSON](g:json)
    -   So common that `requests` has built-in support
-   Unfortunately, there is no standard for representing tabular data as JSON
    -   A list with one list with N column names + N lists of values?
    -   A list with N dictionaries, all with the same keys?
    -   A dictionary with column names and lists of values, all the same length?

<figure id="http_json_tables">
  <img src="http_json_tables.svg" alt="Three ways to represent tables as JSON"/>
  <figcaption>Figure 2: Representing tables as JSON</figcaption>
</figure>

## Local Web Server

-   Pushing files to GitHub so that we can use them is annoying
-   And we want to show how to make things *wrong* so that we can then make them *right*
-   Use Python's [`http.server`][py_http_server] module
    to run a [local server](g:local_server)

```{data-file="local_server.sh"}
python -m http.server -d site
```

-   Host name is [`localhost`](g:localhost)
-   Uses [port](g:port) 8000 by default
    -   So URLs look like `http://localhost:8000/path/to/file`
-   `-d site` tells the server to use `site` as its root directory
-   Use this local server for the next few examples
    -   Build our own server later on to show how it works

## Talk to Local Server

```{data-file="get_local.py"}
import requests

URL = "http://localhost:8000/motto.txt"

response = requests.get(URL)
print(f"status code: {response.status_code}")
print(f"body:\n{response.text}")
```
```{data-file="get_local.out"}
::ffff:127.0.0.1 - - [18/Feb/2024 09:12:24] "GET /motto.txt HTTP/1.1" 200 -
status code: 200
body:
Start where you are, use what you have, help who you can.

```

-   [Concurrent](g:concurrency) systems are hard to debug
    -   Multiple streams of activity
    -   Order may change from run to run
    -   Usually easiest to run each process in its own terminal window

## Our Own File Server

```{data-file="file_server_unsafe.py:do_get"}
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url_path = self.path.lstrip("/")
            full_path = Path.cwd().joinpath(url_path)
            print(f"'{self.path}' => '{full_path}'")
            if not full_path.exists():
                raise ServerException(f"{self.path} not found")
            elif not full_path.is_file():
                raise ServerException(f"{self.path} not file")
            else:
                self.handle_file(self.path, full_path)
        except Exception as msg:
            self.handle_error(msg)
```

-   Our `RequestHandler` handles a single `GET` request
-   Combine working directory with requested file path to get local path to file
-   Return that if it exists and is a file or raise an error

## Support Code

-   Serve files

```{data-file="file_server_unsafe.py:send_content"}
    def send_content(self, content, status):
        self.send_response(int(status))
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)
    ```

-   Handle errors

```{data-file="file_server_unsafe.py:error_page"}
ERROR_PAGE = """\
<html>
  <head><title>Error accessing {path}</title></head>
  <body>
    <h1>Error accessing {path}: {msg}</h1>
  </body>
</html>
"""
```
```{data-file="file_server_unsafe.py:handle_error"}
    def handle_error(self, msg):
        content = ERROR_PAGE.format(path=self.path, msg=msg)
        content = bytes(content, "utf-8")
        self.send_content(content, HTTPStatus.NOT_FOUND)
    ```

-   Define our own exceptions so we're sure we're only catching what we expect

```{data-file="file_server_unsafe.py:exception"}
class ServerException(Exception):
    pass
```

## Running Our File Server

```{data-file="file_server_unsafe.py:main"}
if __name__ == "__main__":
    os.chdir(sys.argv[1])
    serverAddress = ("", 8000)
    server = HTTPServer(serverAddress, RequestHandler)
    print(f"serving in {os.getcwd()}...")
    server.serve_forever()
```

-   And then get `motto.txt` as before

## Built-in Safety

-   Modify `requests` script to take URL as command-line parameter

```{data-file="get_url.py"}
import requests
import sys

URL = sys.argv[1]

response = requests.get(URL)
print(f"status code: {response.status_code}")
print(f"body:\n{response.text}")
```

-   Add a sub-directory to `site` called `sandbox` with a file `example.txt`
    -   Called a [sandbox](g:sandbox) because it's a safe place to play
-   Serve that sub-directory

```{data-file="file_server_sandbox.sh"}
python src/file_server_unsafe.py site/sandbox
```

-   Can get files from that directory

```{data-file="get_url_allowed.sh"}
python src/get_url.py http://localhost:8000/example.txt
```
```{data-file="get_url_allowed_server.out"}
'/example.txt' => '/tut/safety/site/sandbox/example.txt'
127.0.0.1 - - [21/Feb/2024 06:04:32] "GET /example.txt HTTP/1.1" 200 -
```
```{data-file="get_url_allowed_client.out"}
status code: 200
body:
example file
```

-   But not from parent directory (which isn't part of sandbox)

```{data-file="get_url_disallowed.sh"}
python src/requests_local_url.py http://localhost:8000/motto.txt
```
```{data-file="get_url_disallowed_server.out"}
'/motto.txt' => '/tut/safety/site/sandbox/motto.txt'
127.0.0.1 - - [21/Feb/2024 06:04:38] "GET /motto.txt HTTP/1.1" 404 -
```
```{data-file="get_url_disallowed_client.out"}
status code: 404
body:
<html>
  <head><title>Error accessing /motto.txt</title></head>
  <body>
    <h1>Error accessing /motto.txt: /motto.txt not found</h1>
  </body>
</html>
```

-   `requests` strips the leading `..` off the path before sending it
-   And if we try that URL in the browser, same thing happens
-   So we're safe, right?

## Introducing `netcat`

-   [`netcat`][netcat] (often just `nc`) is a computer networking tool
-   Open a connection, send exactly what the user types, and show exactly what is sent in response

```{data-file="nc_localhost.sh"}
nc localhost 8000
```
```{data-file="nc_allowed.text"}
GET /example.txt HTTP/1.1

```
```{data-file="nc_allowed.out"}
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.12.1
Date: Thu, 22 Feb 2024 18:37:37 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 13

example file
```

-   Let's see what happens if we *do* send a URL with `..` in it

```{data-file="nc_disallowed.text"}
GET ../motto.txt HTTP/1.1

```
```{data-file="nc_disallowed.out"}
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.12.1
Date: Thu, 22 Feb 2024 18:38:50 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 58

Start where you are, use what you have, help who you can.
```

-   We shouldn't be able to see files outside the sandbox
-   But if someone doesn't strip out the `..` characters, users can escape

## Exercise {: .exercise}

The shortcut <code>~<em>username</em></code> means
"the specified user's home directory" in the shell,
while `~` on its own means "the current user's home directory".
Create a file called `test.txt` in your home directory
and then try to get `~/test.txt` using your browser,
`requests`,
and `netcat`.
What happens with each and why?

## A Safer File Server

```{data-file="file_server_safe.py:handle_file"}
    def handle_file(self, given_path, full_path):
        try:
            resolved_path = str(full_path.resolve())
            sandbox = str(Path.cwd().resolve())
            if not resolved_path.startswith(sandbox):
                raise ServerException(f"Cannot access {given_path}")
            with open(full_path, "rb") as reader:
                content = reader.read()
            self.send_content(content, HTTPStatus.OK)
        except FileNotFoundError:
            raise ServerException(f"Cannot find {given_path}")
        except IOError:
            raise ServerException(f"Cannot read {given_path}")
    ```

-   [Resolve](g:resolve_path) the constructed path
-   Then check that it's below the current working directory (i.e., the sandbox)
-   And fail if it isn't
    -   Using our own `ServerException` guarantees that all errors are handled the same way

## Exercise {: .exercise}

[Refactor](g:refactor) the `do_GET` and `handle_file` methods in `RequestHandler`
so that all checks are in one place.
Does this make the code easier to understand overall?
Do you think making code easier to understand also makes it safer?

## Serving Data

-   Rarely have JSON lying around as [static files](g:static_file)
-   More common to have either CSV or a database

```{data-file="birds_head.sh"}
head -n 10 site/birds.csv
```
```{data-file="birds_head.out"}
loc_id,latitude,longitude,region,year,month,day,species_id,num
L13476859,60.8606726,-135.2015181,CA-YT,2021,2,1,redcro,3.0
L13476859,60.8606726,-135.2015181,CA-YT,2021,2,1,rebnut,1.0
L13476859,60.8606726,-135.2015181,CA-YT,2021,2,1,comred,13.0
L13476859,60.8606726,-135.2015181,CA-YT,2021,2,1,dowwoo,1.0
L13476859,60.8606726,-135.2015181,CA-YT,2021,2,1,bkcchi,3.0
L13476859,60.8606726,-135.2015181,CA-YT,2021,2,1,haiwoo,1.0
L13476859,60.8606726,-135.2015181,CA-YT,2021,2,8,nobird,
L13476859,60.8606726,-135.2015181,CA-YT,2021,2,15,rebnut,2.0
L13476859,60.8606726,-135.2015181,CA-YT,2021,2,15,bkcchi,3.0
```

-   Modify server to generate it dynamically
-   Main program

```{data-file="bird_server_whole.py:main"}
def main():
    sandbox, filename = sys.argv[1], sys.argv[2]
    os.chdir(sandbox)
    df = pl.read_csv(filename)
    serverAddress = ("", 8000)
    server = BirdServer(df, serverAddress, RequestHandler)
    server.serve_forever()
```

-   Create our own server class because we want to pass the dataframe in the constructor

```{data-file="bird_server_whole.py:server"}
class BirdServer(HTTPServer):
    def __init__(self, data, server_address, request_handler):
        super().__init__(server_address, request_handler)
        self._data = data
```

-   `do_GET` converts the dataframe to JSON (will modify later to do more than this)

```{data-file="bird_server_whole.py:get"}
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        result = self.server._data.write_json(row_oriented=True)
        self.send_content(result, HTTPStatus.OK)
```

-   `send_content` [encodes](g:character_encoding) the JSON string as [UTF-8](g:utf_8)
    and sets the MIME type to `application/json`

```{data-file="bird_server_whole.py:send"}
    def send_content(self, content, status):
        content = bytes(content, "utf-8")
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)
```

-   Can view in browser at `http://localhost:8000` or use `requests` to fetch as before

## Slicing Data

-   URL can contain [query parameters](g:query_parameter)
-   Want `http://localhost:8000/?year=2021&species=rebnut` to select red-breasted nuthatches in 2021
-   Put slicing in a method of its own

```{data-file="bird_server_slice.py:get"}
    def do_GET(self):
        result = self.filter_data()
        as_json = result.to_json(orient="records")
        self.send_content(as_json, HTTPStatus.OK)
    ```

-   Use `urlparse` and `parse_qs` from [`urllib.parse`][py_urllib_parse] to get query parameters
    -   (Key, list) dictionary
-   Then filter data as requested

```{data-file="bird_server_slice.py:filter"}
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
    ```

## Exercise {: .exercise}

1.  Write a function that takes a URL as input
    and returns a dictionary whose keys are the query parameters' names
    and whose values are lists of their values.
    Do you now see why you should use the library function to do this?

2.  Modify the server so that clients can specify which columns they want returned
    as a comma-separated list of names.
    If the client asks for a column that doesn't exist, ignore it.

1.  Modify your solution to the previous exercise so that
    if the client asks for a column that doesn't exist
    the server returns a status code 400 (Bad Request)
    and a JSON blog with two keys:
    `status_code` (set to 400)
    and `error_message` (set to something informative).
    Explain why the server should return JSON rather than HTML in the case of an error.
