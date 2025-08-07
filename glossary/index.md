# Glossary

## A

<span id="access_control">access control</span>
:   FIXME

<span id="ascii">ASCII character encoding</span>
:   A standard way to represent the characters commonly used in the Western
    European languages as 7-bit integers, now largely superceded by
    [Unicode](g:unicode).

<span id="authentication">authentication</span>
:   The act of establishing one's identity.

<span id="authorization">authorization</span>
:   The act of establishing that one has a right to access certain information.

## B

<span id="background_process">background a process</span>
:   To disconnect a [process](g:process) from the terminal but keep it
    running.

<span id="ball_and_stick">ball-and-stick model</span>
:   FIXME

<span id="base64">base64 encoding</span>
:   A representation of binary data that represents each group of 6 bits
    as one of 64 printable characters.

<span id="block_device">"block device"</span>
:   FIXME

<span id="block_filesystem">"block (in filesystem)"</span>
:   FIXME

<span id="buffer_noun">buffer (noun)</span>
:   An area of memory used to hold data temporarily.

<span id="buffer_verb">buffer (verb)</span>
:   To store something in memory temporarily,
    e.g., while waiting for there to be enough data to make an I/O operation worthwhile.

## C

<span id="cache">cache</span>
:   To store a copy of data locally in order to speed up access,
    or the data being stored.

<span id="callback_function">callback function</span>
:   A function A that is passed to another function B so that B can call it at
    some later point.

<span id="capability">capability</span>
:   FIXME

<span id="character_device">"character device"</span>
:   FIXME

<span id="character_encoding">character encoding</span>
:   A way to represent characters as bytes. Common examples include [ASCII](g:ascii)
    and [UTF-8](g:utf_8).

<span id="child_process">child process</span>
:   A [process](g:process) created by another process,
    which is called its [parent process](g:parent_process).

<span id="cleartext">cleartext</span>
:   Text that has not been [encrypted](g:encryption).

<span id="client">client</span>
:   A program such as a browser that sends requests to a server and does something with the response.

<span id="command_interpolation">command interpolation</span>
:   FIXME

<span id="concurrency">concurrency</span>
:   The ability of different parts of a system to take action at the same time.

<span id="copy_on_write">copy-on-write</span>
:   FIXME

## D

<span id="daemon">daemon</span>
:   A long-lived process managed by an operating system
    that provides a service such as printer management to other processes.

<span id="device">device</span>
:   FIXME

<span id="docker">Docker</span>
:   A tool for creating and managing isolated computing environments.

<span id="docker_container">Docker container</span>
:   A particular running (or runnable) instance of a [Docker image](g:docker_image).

<span id="docker_image">Docker image</span>
:   A package containing the software and supporting files [Docker](g:docker) needs
    to run an application in isolation.

<span id="docker_layer">layer (of Docker image)</span>
:   FIXME

<span id="docker_tag">tag (a Docker image)</span>
:   FIXME

<span id="dockerfile">Dockerfile</span>
:   The name usually given to a file containing commands to build a [Docker image](g:docker_image).

<span id="dynamic_content">dynamic content</span>
:   Web site content that is generated on the fly.
    Dynamic content is usually customized according to the requester's identity,
    [query parameter](g:query_parameter),
    etc.

## E

<span id="encryption">encryption</span>
:   The process of converting data from a representation that anyone can read
    to one that can only be read by someone with the right algorithm and/or key.

<span id="env_var">environment variable</span>
:   A [shell variable](g:shell_var) that is inherited by [child processes](g:child_process)

<span id="exit_status">exit status</span>
:   FIXME

## F

<span id="filesystem">filesystem</span>
:   The set of files and directories making up a computer's permanent storage,
    or the software component used to manage them.

<span id="flush">flush</span>
:   To move data from a [buffer](g:buffer_noun) to its intended destination immediately.

<span id="foreground_process">foreground a process</span>
:   To reconnect a [process](g:process) to the terminal after it has
    been [backgrounded](g:background_process) or [suspended](g:suspend_process).

<span id="fork_process">fork (a process)</span>
:   To create a duplicate of an existing [process](g:process),
    typically in order to run a new program.

## G

<span id="gid">group ID (GID)</span>
:   FIXME

## H

<span id="hash">hash</span>
:   FIXME

<span id="hostname">hostname</span>
:   A human-readable name for a computer on a network.

<span id="http">HTTP</span>
:   full: HyperText Transfer Protocol
    The protocol used to exchange information between browsers and websites,
    and more generally between other clients and servers.
    Communication consists of [requests](g:http_request) and [responses](g:http_response).

<span id="http_header">header (of HTTP request or response)</span>
:   A name-value pair at the start of an [HTTP request](g:http_request) or [response](g:http_response).
    Headers are used to specify what data formats the sender can handle,
    the date and time the message was sent,
    and so on.

<span id="http_method">HTTP method</span>
:   The verb in an [HTTP request](g:http_request) that defines what the [client](g:client) wants to do.
    Common methods are `GET` (to get data) and `POST` (to submit data).

<span id="http_request">HTTP request</span>
:   A precisely-formatted block of text sent from a [client](g:client) such as a browser
    to a [server](g:server)
    that specifies what resource is being requested,
    what data formats the client will accept, etc.

<span id="http_response">HTTP response</span>
:   A precisely-formatted block of text sent from a [server](g:server)
    back to a [client](g:client) in reply to a [request](g:http_request).

<span id="http_status_code">HTTP status code</span>
:   A numerical code that indicates what happened when an [HTTP request](g:http_request) was processed,
    such as 200 (OK),
    404 (not found),
    or 500 (internal server error).

## I

<span id="inode">inode</span>
:   FIXME

## J

<span id="json">JavaScript Object Notation (JSON)</span>
:   A way to represent data by combining basic values like numbers
    and character strings in lists and key-value structures. Unlike
    other formats, it is unencumbered by a syntax for writing comments.

## K

## L

<span id="link_hard">hard link (in filesystem)</span>
:   FIXME

<span id="link_sym">symbolic link (in filesystem)</span>
:   FIXME

<span id="lint">lint</span>
:   FIXME

<span id="local_server">local server</span>
:   A [server](g:server) running on the programmer's own computer,
    typically for development purposes.

<span id="localhost">localhost</span>
:   A special [host name](g:hostname) that identifies
    the computer that the software is running on.

## M

<span id="mime_type">MIME type</span>
:   A standard that defines types of file content,
    such as `text/plain` for plain text and `image/jpeg` for JPEG images.

<span id="mount">mount</span>
:   FIXME

## N

<span id="name_collision">name collision</span>
:   The problem that occurs when two different applications use the same name
    for different things.

## O

<span id="octal">octal</span>
:   FIXME

<span id="operating_system">operating system (OS)</span>
:   A program whose job is to manage the hardware of a computer.
    Other programs interact with the OS through [system calls](g:system_call).

## P

<span id="parent_process">parent process</span>
:   A [process](g:process) which has created one or more other processes,
    which are called its [child processes](g:child_process).

<span id="path">path (in filesystem)</span>
:   An expression that refers to a file or directory in a filesystem.

<span id="port">port</span>
:   A logical endpoint for communication,
    like a phone number in an office building.

<span id="process">process</span>
:   A running instance of a program.

<span id="process_id">process ID</span>
:   The unique numerical identifier of a running [process](g:process).

<span id="process_tree">process tree</span>
:   The set of processes created directly or indirectly by one process
    and the [parent](g:parent_process)-[child](g:child_process) relationships between them.

## Q

<span id="query_parameter">query parameter</span>
:   A key-value pair included in a URL that the server may use to modify or customize its response.

## R

<span id="refactor">refactor</span>
:   To reorganize code without changing its overall behavior.

<span id="resume_process">resume (a process)</span>
:   To continue the execution of a [suspended](g:suspend_process) [process](g:process).

<span id="resolve_path">resolve (a path)</span>
:   To translate a [path](g:path) into the canonical name of the file or directory it refers to.

<span id="root_directory">root directory</span>
:   The top-most directory in the [filesystem](g:filesystem)
    that contains all other directories and files.

<span id="root_user">root (user account)</span>
:   The usual ID of the [superuser](g:superuser) account on a computer.

## S

<span id="sandbox">sandbox</span>
:   An isolated computing environment in which operations can be executed safely.

<span id="server">server</span>
:   A program that waits for requests from [clients](g:client)
    and sends them data in response.

<span id="shell">shell</span>
:   A program that allows a user to interact with a computer's operating system
    and other programs through a textual user interface.

<span id="shell_script">shell_script</span>
:   A program that uses [shell](g:shell) commands as its programming language.

<span id="shell_var">shell variable</span>
:   A variable set and used in the [shell](g:shell).

<span id="signal">signal</span>
:   A message sent to a running [process](g:process) separate from its
    normal execution, such as an interrupt or a timer notification.

<span id="signal_handler">signal handler</span>
:   A [callback function](g:callback_function) that is called when
    a [process](g:process) receives a [signal](g:signal).

<span id="source_shell">source (in shell script)</span>
:   To run one [shell script](g:shell_script) in the same process as another.

<span id="static_file">static file</span>
:   Web site content that is stored as a file on disk that is served as-is.
    Serving static files is usually faster than generating [dynamic content](g:dynamic_content),
    but can only be done if what's wanted is unchanging and known in advance.

<span id="superuser">superuser</span>
:   An administrative account on a computer that has permission
    to see, change, and run everything.

<span id="suspend_process">suspend (a process)</span>
:   To pause the execution of a [process](g:process) but leave it intact so that it
    can [resume](g:resume_process) later.

<span id="system_call">system call</span>
:   A call to one of the functions provided by an [operating system](g:operating_system).

## T

## U

<span id="uid">user ID (UID)</span>
:   FIXME

<span id="unicode">Unicode</span>
:   A standard that defines numeric codes for many thousands of characters and
    symbols. Unicode does not define how those numbers are stored; that is
    done by standards like [UTF-8](g:utf_8).

<span id="user_group">user group</span>
:   FIXME

<span id="utf_8">UTF-8</span>
:   A way to store the numeric codes representing [Unicode](g:unicode)
    characters that is backward-compatible with the older [ASCII](g:ascii) standard.

<span id="uuid">Universally Unique Identifier (UUID)</span>
:   FIXME

## V

<span id="virtual_env">virtual environment</span>
:   A set of libraries, applications, and other resources that are isolated from the main system
    and other virtual environments.

## W

<span id="web_scraping">web scraping</span>
:   The act of extracting data from HTML pages on the web.

## X

## Y

## Z
