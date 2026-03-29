# Authentication

## The Three A's Revisited

-   The filesystem chapter introduced authentication, authorization, and access control
-   This chapter focuses on authentication: how the system establishes who you are
-   Authentication is always a claim followed by evidence
    -   "I am Ning" — but how does the system verify that?
-   Two classic approaches:
    -   Something you know (password, PIN)
    -   Something you have (a key, a hardware token, a phone)
    -   Something you are (fingerprint, face — biometrics)
-   Real systems increasingly combine more than one (multi-factor authentication)

## User Accounts on Unix

-   Unix stores user account information in `/etc/passwd`
    -   Readable by everyone (programs need to look up user names)
    -   One line per account, colon-separated fields

```{data-file="etc_passwd.text"}
$ grep tut /etc/passwd
tut:x:501:20:Tutorial User:/Users/tut:/bin/bash
```

-   Fields in order: username, password placeholder, UID, GID, comment, home directory, shell
-   The `x` in the password field means "look in /etc/shadow instead"
    -   Historically passwords were stored here — hence the name "passwd"
    -   Moving them to `/etc/shadow` was a security improvement

## Password Storage

-   Passwords are never stored as [cleartext](g:cleartext)
    -   If the file is leaked, attackers would have everyone's password immediately
-   Instead, the system stores a [hash](g:hash) of the password
    -   A one-way function: easy to compute hash from password, infeasible to reverse
    -   Deterministic: same password always produces same hash
-   When you log in:
    1.  You type your password
    2.  The system hashes what you typed
    3.  It compares the result to the stored hash
    4.  If they match, you are authenticated
-   `/etc/shadow` stores the hashed passwords; only readable by root

```{data-file="etc_shadow.text"}
$ sudo cat /etc/shadow | grep tut
tut:$6$rounds=656000$salt$hashedvalue...:19831:0:99999:7:::
```

-   The hash field encodes:
    -   `$6$` — hashing algorithm (6 = SHA-512)
    -   `$rounds=656000$` — work factor (how many iterations)
    -   `$salt$` — random value mixed in before hashing (see below)
    -   The actual hash

## Salts and Rainbow Tables

-   A [salt](g:salt) is a random value stored alongside the hash
    -   Before hashing, concatenate the salt and the password
    -   Same password + different salt = different hash
-   Why bother?
    -   Without salts, attackers can pre-compute a table of (password → hash) pairs
    -   Called a "rainbow table"
    -   With salts, the attacker must redo the computation for each account separately
-   In Python, `hashlib` provides low-level hashing;
    use `passlib` or `bcrypt` for password storage in real applications

```{data-file="hash_example.py"}
import hashlib
import os

# Low-level: do not use this directly for passwords
password = "correct horse battery staple"
salt = os.urandom(16)
hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 260000)
print(f"salt: {salt.hex()}")
print(f"hash: {hashed.hex()}")
```

-   `pbkdf2_hmac` is a "slow" hash function — intentionally expensive to compute
    -   Makes brute-force attacks much slower
    -   The 260000 is the iteration count; higher = slower to crack, also slower to verify

<section class="exercise" markdown="1">

## Exercise: Hash Properties

1.  Run the hash example above twice.
    Are the outputs the same?
    Why or why not?

2.  Change the password by one character and re-run.
    How does the hash change?
    What property of hash functions does this illustrate?

</section>

## sudo and su

-   Principle of least privilege: run processes with only the permissions they need
-   `su username` — substitute user; switches to another account for the rest of the session
    -   Requires the *target* user's password (or root password)
    -   `su -` starts a fresh login shell as that user

```{data-file="su_example.text"}
$ whoami
tut

$ su nobody
Password:
$ whoami
nobody

$ exit
$ whoami
tut
```

-   `sudo command` — runs a single command as root (or another specified user)
    -   Configured in `/etc/sudoers`
    -   Uses *your* password, not root's
    -   Actions are logged (unlike `su`)

```{data-file="sudo_example.text"}
$ cat /etc/shadow
cat: /etc/shadow: Permission denied

$ sudo cat /etc/shadow | head -n 3
root:*:19810:0:99999:7:::
daemon:*:19810:0:99999:7:::
tut:$6$rounds=656000$...
```

-   `/etc/sudoers` controls who can run what as whom

```{data-file="sudoers_example.text"}
# Allow tut to run any command as root (with password)
tut ALL=(ALL) ALL

# Allow deploy user to restart nginx without a password
deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```

-   Use `visudo` to edit `/etc/sudoers` — it validates syntax before saving

<section class="exercise" markdown="1">

## Exercise: sudo Logging

1.  Run `sudo ls /root` and then look at the system log (try `/var/log/auth.log`
    on Linux or `log show --predicate 'process == "sudo"'` on macOS).
    What information is recorded?

2.  Why is logging important for `sudo` but less important for `su`?

</section>

## Windows Authentication

-   Windows stores local account credentials in the Security Account Manager (SAM) database
    -   Located at `C:\Windows\System32\config\SAM`
    -   Locked while Windows is running; readable only by the SYSTEM account
-   Passwords are hashed with NTLM (NT LAN Manager)
    -   Historically used MD4 (now considered weak)
    -   Modern Windows also stores a more recent hash format
-   Domain environments use Active Directory (AD)
    -   Kerberos protocol for authentication tickets
    -   Single sign-on across machines in the domain
-   Windows equivalents of Unix tools:

| Unix       | Windows equivalent      | Purpose                          |
| ---------- | ----------------------- | -------------------------------- |
| `su`       | `runas /user:name cmd`  | Run command as another user      |
| `sudo`     | UAC elevation prompt    | Temporarily raise privileges     |
| `id`       | `whoami /all`           | Show current user and groups     |
| `passwd`   | `net user name *`       | Change a user's password         |
| `useradd`  | `net user name /add`    | Create a new user account        |

-   User Account Control (UAC) is Windows' version of least-privilege enforcement
    -   Prompts when a program requests elevated privileges
    -   Can be suppressed (but shouldn't be) for automation

## SSH Key Pairs

-   Password authentication has weaknesses
    -   Passwords can be guessed, phished, or intercepted
    -   Typing a password into a remote terminal exposes it to the remote machine
-   Public key cryptography provides an alternative
    -   Generate a key pair: a private key (keep secret) and a public key (share freely)
    -   Something encrypted with the public key can only be decrypted with the private key
    -   Something signed with the private key can be verified with the public key
-   For SSH: server challenges the client to prove it has the private key
    -   Without ever transmitting the private key

```{data-file="ssh_keygen.text"}
$ ssh-keygen -t ed25519 -C "tut@example.com"
Generating public/private ed25519 key pair.
Enter file in which to save the key (/Users/tut/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Your identification has been saved in /Users/tut/.ssh/id_ed25519
Your public key has been saved in /Users/tut/.ssh/id_ed25519.pub
```

-   `ed25519` is the recommended key type (newer and more secure than RSA)
-   Add a passphrase to protect the private key if it is ever stolen
-   Copy the public key to the remote server

```{data-file="ssh_copy_id.text"}
$ ssh-copy-id -i ~/.ssh/id_ed25519.pub tut@remote.example.com
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s)
Number of key(s) added:        1
```

-   This appends the public key to `~/.ssh/authorized_keys` on the remote machine
-   SSH agent avoids re-typing the passphrase in each session

```{data-file="ssh_agent.text"}
$ eval $(ssh-agent)
Agent pid 12345

$ ssh-add ~/.ssh/id_ed25519
Enter passphrase for /Users/tut/.ssh/id_ed25519:
Identity added: /Users/tut/.ssh/id_ed25519

$ ssh tut@remote.example.com
# No passphrase prompt — agent handles it
```

-   Configure SSH behaviour in `~/.ssh/config`

```{data-file="ssh_config.text"}
Host remote
    HostName remote.example.com
    User tut
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent no
```

-   After this, `ssh remote` is equivalent to `ssh -i ~/.ssh/id_ed25519 tut@remote.example.com`

<section class="exercise" markdown="1">

## Exercise: Key Inspection

1.  Generate a key pair with `ssh-keygen`.
    What files are created?
    What do the contents of the public key file look like?

2.  What does the `ForwardAgent no` setting in `~/.ssh/config` do,
    and why might you want to keep it disabled on untrusted hosts?

</section>

## Data Authentication: Hashing and HMAC

-   Authentication is not only about who you are — it can also mean verifying data integrity
    -   "Did this file arrive without modification?"
    -   "Did this message really come from who it claims to?"
-   Checksums let you verify a file hasn't changed (accidentally or maliciously)

```{data-file="checksum.text"}
$ sha256sum site/birds.csv
3f2a... site/birds.csv

$ sha256sum site/birds.csv
3f2a... site/birds.csv

$ echo "extra" >> site/birds.csv
$ sha256sum site/birds.csv
9b1c... site/birds.csv   ← different hash
```

-   A plain hash proves the data is unchanged, but not *who* produced it
-   An [HMAC](g:hmac) (Hash-based Message Authentication Code) uses a shared secret key

```{data-file="hmac_example.py"}
import hashlib
import hmac

key = b"shared-secret-key"
message = b"the data we are authenticating"

mac = hmac.new(key, message, hashlib.sha256).hexdigest()
print(f"HMAC: {mac}")

# Verify: recompute and compare
expected = hmac.new(key, message, hashlib.sha256).digest()
received = bytes.fromhex(mac)
print(f"valid: {hmac.compare_digest(expected, received)}")
```

-   Use `hmac.compare_digest` rather than `==` to prevent timing attacks
    -   `==` short-circuits on the first mismatch, leaking timing information
    -   `compare_digest` always takes the same amount of time

## Multi-Factor Authentication

-   Even strong passwords can be stolen; SSH keys can be copied
-   Multi-factor authentication (MFA) requires two or more independent factors
    -   Something you know + something you have is most common
-   TOTP (Time-Based One-Time Password) is the mechanism behind authenticator apps
    -   Server and app share a secret key
    -   Every 30 seconds, both compute `HMAC(secret, current_time // 30)`
    -   The app displays the result; you type it in
    -   An intercepted code is useless after 30 seconds
-   Hardware security keys (e.g., YubiKey) are more phishing-resistant
    -   They verify the domain of the site before responding

```{data-file="totp_example.py"}
import pyotp
import time

# Server-side: generate a shared secret once and store it
secret = pyotp.random_base32()
print(f"secret (store securely): {secret}")

# App-side: generate a code using the secret and current time
totp = pyotp.TOTP(secret)
code = totp.now()
print(f"current code: {code}")

# Server-side: verify a submitted code
print(f"valid: {totp.verify(code)}")
```

-   Never implement your own TOTP: use a well-tested library
