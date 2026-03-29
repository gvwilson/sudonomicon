# Networking

## What Is a Network?

-   A network is a set of computers that can send data to each other
-   The internet is a network of networks
    -   Your home router connects your local network to your ISP's network
    -   ISPs are connected to backbone providers
    -   Every packet travels through many intermediate machines
-   Key insight: you do not need to understand the physical layer (cables, WiFi)
    -   Protocols at higher layers make different hardware look the same to programs

## IP Addresses

-   Every device on a network has an [IP address](g:ip_address)
-   IPv4: four bytes written as four decimal numbers separated by dots
    -   Example: `192.168.1.42`
    -   About 4 billion possible addresses — nearly exhausted
-   IPv6: sixteen bytes written as eight groups of four hex digits separated by colons
    -   Example: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`
    -   Leading zeroes and consecutive zero groups can be compressed: `2001:db8::1`
    -   340 undecillion addresses — not running out soon
-   Special addresses:
    -   `127.0.0.1` (IPv4) or `::1` (IPv6): the loopback address, always means "this machine"
    -   `192.168.x.x`, `10.x.x.x`, `172.16.x.x–172.31.x.x`: private ranges (RFC 1918)
        -   Not routable on the public internet; used inside home/office networks
    -   `0.0.0.0`: "any local address" (used when binding a server)

```{data-file="show_ip.text"}
$ hostname -I           # Linux
192.168.1.42 fd00::1

$ ipconfig getifaddr en0  # macOS
192.168.1.42

$ ipconfig              # Windows
   IPv4 Address . . . . . : 192.168.1.42
```

## Ports

-   An IP address identifies a machine; a [port](g:port) identifies a service on that machine
    -   Like a street address vs. an apartment number
-   A 16-bit number: 0 to 65535
-   Well-known ports (0–1023): reserved for standard services, require root to bind

| Port | Service    |
| ---- | ---------- |
|   22 | SSH        |
|   25 | SMTP       |
|   53 | DNS        |
|   80 | HTTP       |
|  443 | HTTPS      |
| 5432 | PostgreSQL |
| 3306 | MySQL      |

-   Registered ports (1024–49151): assigned to specific applications by IANA
-   Ephemeral ports (49152–65535): assigned dynamically to clients by the OS
-   Use `netstat -an` or `ss -tulnp` to see which ports are in use

```{data-file="netstat_example.text"}
$ netstat -an | grep LISTEN | head -n 5
tcp4   0   0   127.0.0.1.5432    *.*     LISTEN
tcp4   0   0   *.8000            *.*     LISTEN
tcp6   0   0   *.22              *.*     LISTEN
```

## TCP vs. UDP

-   Two main transport protocols sit on top of IP
-   TCP (Transmission Control Protocol):
    -   Connection-oriented: both sides perform a three-way handshake before data flows
    -   Reliable: every packet is acknowledged; lost packets are retransmitted
    -   Ordered: packets are reassembled in the right order even if they arrive out of order
    -   Used by HTTP, HTTPS, SSH, SMTP, PostgreSQL
-   UDP (User Datagram Protocol):
    -   Connectionless: send a packet and hope it arrives
    -   Unreliable: no acknowledgment, no retransmission
    -   Ordered delivery is not guaranteed
    -   Much lower overhead — useful when speed matters more than reliability
    -   Used by DNS (queries), video streaming, online games, NTP

```{data-file="tcp_udp_comparison.text"}
Think of TCP as a phone call:
  - You dial, the other end picks up (handshake)
  - Both sides take turns talking (ordered, reliable)
  - Either side can hang up gracefully (teardown)

Think of UDP as sending a postcard:
  - You write an address and drop it in a box
  - No confirmation it arrived
  - Very fast and simple
```

## Sockets

-   A [socket](g:socket) is one endpoint of a network connection
    -   Identified by: protocol + IP address + port number
    -   Two sockets (one each end) make a connection
-   Python's `socket` module provides direct access

```{data-file="tcp_server.py"}
import socket

HOST = "127.0.0.1"
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"listening on {HOST}:{PORT}")
    conn, addr = server.accept()
    with conn:
        print(f"connected from {addr}")
        data = conn.recv(1024)
        conn.sendall(data)   # echo it back
```

```{data-file="tcp_client.py"}
import socket

HOST = "127.0.0.1"
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    client.sendall(b"hello from client")
    data = client.recv(1024)
    print(f"received: {data!r}")
```

-   `AF_INET`: use IPv4; use `AF_INET6` for IPv6 or `AF_INET` with the right address for both
-   `SOCK_STREAM`: TCP; `SOCK_DGRAM` for UDP
-   `SO_REUSEADDR`: allow re-binding a port immediately after the previous server exits
-   Most applications use higher-level libraries (`http.server`, `requests`, `flask`)
    rather than raw sockets

<section class="exercise" markdown="1">

## Exercise: Echo Server

1.  Run the TCP server in one terminal and the client in another.
    What do you see on each side?

2.  Modify the server to handle multiple clients in sequence
    (add a `while True` loop around `server.accept()`).
    What happens if two clients connect at the same time?

</section>

## DNS: Domain Name System

-   Humans remember names (`github.com`); computers communicate via IP addresses
-   [DNS](g:dns) is the distributed system that translates between them
-   Organized as a hierarchy:
    -   Root (`.`) → top-level domain (`.com`, `.org`, `.ca`) → domain (`github`) → subdomain (`api`)
    -   Responsibility for each level is delegated to different servers

## DNS Record Types

-   DNS stores several kinds of records

| Type  | Purpose                                    | Example                             |
| ----- | ------------------------------------------ | ----------------------------------- |
| A     | hostname → IPv4 address                    | `example.com → 93.184.216.34`       |
| AAAA  | hostname → IPv6 address                    | `example.com → 2606:2800:220:1::68` |
| CNAME | alias → canonical hostname                 | `www.example.com → example.com`     |
| MX    | mail exchange for a domain                 | `example.com → mail.example.com`    |
| TXT   | arbitrary text (verification, SPF records) | `"v=spf1 include:..."`              |
| NS    | authoritative name servers for a domain    | `example.com → ns1.example.com`     |

## How DNS Resolution Works

-   When you look up `api.github.com`:
    1.  Check local cache (OS or stub resolver)
    2.  Check `/etc/hosts` (local overrides — useful for development)
    3.  Ask the configured resolver (usually your router or ISP's DNS, e.g., `8.8.8.8`)
    4.  Resolver asks a root server: "who handles `.com`?"
    5.  Resolver asks the `.com` TLD server: "who handles `github.com`?"
    6.  Resolver asks GitHub's authoritative server: "what is `api.github.com`?"
    7.  Answer is returned and cached at each level for the record's TTL (time to live)
-   Most lookups are answered from cache and take a few milliseconds

```{data-file="etc_hosts.text"}
# Add to /etc/hosts for local development:
127.0.0.1   myapp.local
127.0.0.1   api.myapp.local
```

## Querying DNS from the Command Line

```{data-file="dig_example.text"}
$ dig example.com A

;; ANSWER SECTION:
example.com.    3600  IN  A  93.184.216.34

$ dig example.com MX

;; ANSWER SECTION:
example.com.  3600  IN  MX  0 .

$ dig +short github.com
140.82.114.4
```

-   `dig` (Domain Information Groper) is the standard DNS debugging tool
-   `+short` gives a terse answer
-   `nslookup` is available on Windows as well as Unix

```{data-file="reverse_dns.text"}
$ dig -x 93.184.216.34 +short
93.184.216.34.in-addr.arpa domain name pointer example.com.
```

-   Reverse DNS: look up the hostname for an IP address
-   Uses PTR records, stored under `in-addr.arpa`

## DNS in Python

```{data-file="dns_python.py"}
import socket

# Forward lookup: hostname → IP address
ip = socket.gethostbyname("example.com")
print(f"example.com → {ip}")
# example.com → 93.184.216.34

# Returns all addresses and aliases (useful for hosts with multiple IPs)
hostname, aliases, addresses = socket.gethostbyname_ex("github.com")
print(f"hostname: {hostname}")
print(f"addresses: {addresses}")

# Reverse lookup: IP address → hostname
name, _, _ = socket.gethostbyaddr("93.184.216.34")
print(f"93.184.216.34 → {name}")
```

-   For more control (specific record types, custom resolvers), use the `dnspython` package

```{data-file="dnspython_example.py"}
import dns.resolver

answers = dns.resolver.resolve("example.com", "MX")
for rdata in answers:
    print(f"priority {rdata.preference}: {rdata.exchange}")
```

<section class="exercise" markdown="1">

## Exercise: DNS Exploration

1.  Use `dig` to find all the MX records for a domain you use regularly.
    What do the priority numbers mean?

2.  Add an entry to `/etc/hosts` that maps `test.local` to `127.0.0.1`.
    Confirm you can `ping test.local`.
    What does this tell you about the order in which lookups are tried?

3.  What is the TTL on the A record for `github.com`?
    How does TTL affect how quickly DNS changes propagate?

</section>

## Network Troubleshooting

-   `ping host`: send ICMP echo requests to check if a host is reachable
    -   Measures round-trip time; reports packet loss
    -   Some hosts block ICMP, so no response does not always mean unreachable
-   `traceroute host` (Unix) / `tracert host` (Windows): show the path packets take
    -   Each line is one hop (router) along the route
    -   Useful for diagnosing where a connection slows down or breaks

```{data-file="traceroute_example.text"}
$ traceroute github.com
 1  router.local (192.168.1.1)         1.2 ms
 2  10.0.0.1 (10.0.0.1)               8.4 ms
 3  ae-3.r01.tor01.net (206.x.x.x)   15.1 ms
…
12  lb-140-82-114-4-iad.github.com    22.8 ms
```

-   `curl -I url`: send an HTTP HEAD request; shows response headers without body
    -   Useful for checking HTTP status codes, redirects, and Content-Type
-   `netstat -an` / `ss -tulnp`: list open ports and active connections
-   `lsof -i :8000`: show which process is using port 8000 (macOS/Linux)

<section class="exercise" markdown="1">

## Exercise: Following a Request

Use the tools above to trace what happens when you access a familiar website:

1.  Use `dig` to find its IP address.
2.  Use `ping` to check latency to that IP.
3.  Use `traceroute` to see the path.
4.  Use `curl -I` to inspect the HTTP headers.

Do any of the hops in `traceroute` show `* * *`?
What does that mean?

</section>
