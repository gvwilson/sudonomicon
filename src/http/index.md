---
title: "HTTP"
tagline: "Moving data from place to place."
---

## Start with Something Simple

[%inc get_remote.py %]
[%inc get_remote.out %]

-   Use the [`requests`][requests] module to send an [%g http "HTTP" %] [%g http_request "request" %]
-   The URL identifies the file we want
    -   Though as we'll see, the server can interpret it differently
-   Response includes:
    -   [%g http_status_code "HTTP status code" %] such as 200 (OK) or 404 (Not Found)
    -   The text of the response

## What Just Happened

-   [%f http_lifecycle %] shows what happened

[% figure
   slug="http_lifecycle"
   img="http_lifecycle.svg"
   alt="HTTP request/response lifecycle"
   caption="Lifecycle of an HTTP request and response"
%]

-   Open a connection to the server
-   Send an [%g http_request "HTTP request" %] for the file we want
-   Server creates a [%g http_response "response" %] that includes the contents of the file
-   Sends it back
-   `requests` parses the response and creates a Python object for us

## Request Structure

[%inc dump_structure.py %]
[%inc dump_structure.out %]

-   First line is [%g http_method "method" %], URL, and protocol version
-   Every HTTP request can have [%g http_header "headers" %] with extra information
    -   And optionally data being uploaded
-   Yes, it's all just text
    -   Except for uploaded data, which is just bytes

## Response Structure

[%inc response_headers.py %]
[%inc response_headers.out %]

-   Every HTTP response also has with extra information
    -   Does *not* include status code: that appears in the first line
-   Most important for now are:
    -   `Content-Length`: number of bytes in response data (i.e., how much to read)
    -   `Content-Type`: [%g mime_type "MIME type" %] of data (e.g., `text/plain`)
-   From now on we will only show interesting headers

## Exercise {: .exercise}

1.  Add header called `Studying` with the value `safety`
    to the `requests` script shown above.
    Does it make a difference to the response?
    Should it?

1.  What is the difference between the `Content-Type` and the `Content-Encoding` headers?

## When Things Go Wrong

[%inc get_404.py %]
[%inc get_404.out %]

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

[%inc get_json.py %]
[%inc get_json.out %]

-   Parsing data out of HTML is called [%g web_scraping "web scraping" %]
    -   Painful and error prone
-   Better to have the server return data as data
    -   Preferred format these days is [%g json "JSON" %]
    -   So common that `requests` has built-in support
-   Unfortunately, there is no standard for representing tabular data as JSON [%f http_json_tables %]
    -   A list with one list with N column names + N lists of values?
    -   A list with N dictionaries, all with the same keys?
    -   A dictionary with column names and lists of values, all the same length?

[% figure
   slug="http_json_tables"
   img="http_json_tables.svg"
   alt="Three ways to represent tables as JSON"
   caption="Representing tables as JSON"
%]

## Exercise {: .exercise}

Write a `requests` script that gets the current location and crew roster
of [the International Space Station][iss_api].

## Local Web Server

-   Pushing files to GitHub so that we can use them is annoying
-   And we want to show how to make things *wrong* so that we can then make them *right*
-   Use Python's [`http.server`][py_http_server] module
    to run a [%g local_server "local server" %]

[%inc local_server.sh %]

-   Host name is [%g localhost "`localhost`" %]
-   Uses [%g port "port" %] 8000 by default
    -   So URLs look like `http://localhost:8000/path/to/file`
-   `-d site` tells the server to use `site` as its root directory
-   Use this local server for the next few examples
    -   Build our own server later on to show how it works

## Talk to Local Server

[%inc get_local.py %]
[%inc get_local.out %]

-   [%g concurrency "Concurrent" %] systems are hard to debug
    -   Multiple streams of activity
    -   Order may change from run to run
    -   Usually easiest to run each process in its own terminal window

## Our Own File Server

[%inc file_server_unsafe.py mark=do_get %]

-   Our `RequestHandler` handles a single `GET` request
-   Combine working directory with requested file path to get local path to file
-   Return that if it exists and is a file or raise an error

## Support Code

-   Serve files

[%inc file_server_unsafe.py mark=send_content %]

-   Handle errors

[%inc file_server_unsafe.py mark=error_page %]
[%inc file_server_unsafe.py mark=handle_error %]

-   Define our own exceptions so we're sure we're only catching what we expect

[%inc file_server_unsafe.py mark=exception %]

## Running Our File Server

[%inc file_server_unsafe.py mark=main %]

-   And then get `motto.txt` as before

## Built-in Safety

-   Modify `requests` script to take URL as command-line parameter

[%inc get_url.py %]

-   Add a sub-directory to `site` called `sandbox` with a file `example.txt`
    -   Called a [%g sandbox "sandbox" %] because it's a safe place to play
-   Serve that sub-directory

[%inc file_server_sandbox.sh %]

-   Can get files from that directory

[%inc get_url_allowed.sh %]
[%inc get_url_allowed_server.out %]
[%inc get_url_allowed_client.out %]

-   But not from parent directory (which isn't part of sandbox)

[%inc get_url_disallowed.sh %]
[%inc get_url_disallowed_server.out %]
[%inc get_url_disallowed_client.out %]

-   `requests` strips the leading `..` off the path before sending it
-   And if we try that URL in the browser, same thing happens
-   So we're safe, right?

## Introducing netcat

-   [`netcat`][netcat] (often just `nc`) is a computer networking tool
-   Open a connection, send exactly what the user types, and show exactly what is sent in response

[%inc nc_localhost.sh %]
[%inc nc_allowed.text %]
[%inc nc_allowed.out %]

-   Let's see what happens if we *do* send a URL with `..` in it

[%inc nc_disallowed.text %]
[%inc nc_disallowed.out %]

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

[%inc file_server_safe.py mark=handle_file %]

-   [%g resolve_path "Resolve" %] the constructed path
-   Then check that it's below the current working directory (i.e., the sandbox)
-   And fail if it isn't
    -   Using our own `ServerException` guarantees that all errors are handled the same way

## Exercise {: .exercise}

[%g refactor "Refactor" %] the `do_GET` and `handle_file` methods in `RequestHandler`
so that all checks are in one place.
Does this make the code easier to understand overall?
Do you think making code easier to understand also makes it safer?

## Serving Data

-   Rarely have JSON lying around as [%g static_file "static files" %]
-   More common to have either CSV or a database

[%inc birds_head.sh %]
[%inc birds_head.out %]

-   Modify server to generate it dynamically
-   Main program

[%inc bird_server_whole.py mark=main %]

-   Create our own server class because we want to pass the dataframe in the constructor

[%inc bird_server_whole.py mark=server %]

-   `do_GET` converts the dataframe to JSON (will modify later to do more than this)

[%inc bird_server_whole.py mark=get %]

-   `send_content` [%g character_encoding "encodes" %] the JSON string as [%g utf_8 "UTF-8" %]
    and sets the MIME type to `application/json`

[%inc bird_server_whole.py mark=send %]

-   Can view in browser at `http://localhost:8000` or use `requests` to fetch as before

## Slicing Data

-   URL can contain [%g query_parameter "query parameters" %]
-   Want `http://localhost:8000/?year=2021&species=rebnut` to select red-breasted nuthatches in 2021
-   Put slicing in a method of its own

[%inc bird_server_slice.py mark=get %]

-   Use `urlparse` and `parse_qs` from [`urllib.parse`][py_urllib_parse] to get query parameters
    -   (Key, list) dictionary
-   Then filter data as requested

[%inc bird_server_slice.py mark=filter %]

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
