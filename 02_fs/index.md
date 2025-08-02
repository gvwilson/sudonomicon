# The Filesystem

-   FIXME

## Definitions

-   [Ball-and-stick model](g:ball_and_stick)
    -   Computer's hard drive has files and directories
    -   Directories can contain other directories but don't contain data
    -   Files contain data but can't contain other files (or directories)
    -   Everything forms a tree under the [root directory](g:root_directory) `/`
-   More accurate model
    -   Computer may have many storage devices, each with its own [filesystem](g:filesystem)
    -   Each file is made up of one or more fixed-size [blocks](g:block_filesystem)
    -   The filesystem keeps track of which blocks belong to which files
        -   Adds or recycles blocks as necessary
    -   A directory is a special kind of file that keeps track of other files
        -   Files aren't physically "in" a directory

## Information About Files and Directories

-   `ls` command flags:
    -   `-a`: show directories whose names begin with `.`
    -   `-i`: show inode numbers
    -   `-l`: long form (i.e., include several pieces of information)
    -   `-s`: show the number of blocks

```{data-file="ls_long_tmp.sh"}
ls -a -i -l -s tmp
```
```{data-file="ls_long_tmp.out"}
total 8
99138261 0 drwxr-xr-x   3 tut  staff   96 Apr 20 07:50 ./
94560701 0 drwxr-xr-x  22 tut  staff  704 Apr 20 07:53 ../
99138262 8 -rw-r--r--   1 tut  staff  174 Apr 20 07:50 bibliography.html
```

-   It's a shame there's no option for column titles, but we can add them manually

| inode    | blocks | permissions | links | owner | group | bytes | date         | name              |
| -------- | ------ | ----------- | ----- | ----- | ----- | ----- | ------------ | ----------------- |
| 99138261 | 0      | drwxr-xr-x  |     3 | tut   | staff |    96 | Apr 20 07:50 | ./                |
| 94560701 | 0      | drwxr-xr-x  |    22 | tut   | staff |   704 | Apr 20 07:53 | ../               |
| 99138262 | 8      | -rw-r--r--  |     1 | tut   | staff |   174 | Apr 20 07:50 | bibliography.html |

-   The [inode](g:inode) stores attributes and IDs of disk blocks
    -   No-one is sure any longer what the "i" stands for
    -   Each inode has a unique ID that stays the same despite renaming
    -   Design pattern: always generate and manage your own IDs
-   Number of blocks
    -   Each block is typically 4kbyte, but that may vary
    -   FIXME: why 8 blocks for bibliography which is only 174 bytes?
-   Permissions (discussed below)
-   Number of [hard links](g:link_hard)
    -   I.e., the number of things that point to this file or directory
    -   Also discussed below
-   Names of user and group that own the file or directory
    -   Also discussed below
-   Size in bytes (i.e., what `wc -c` reports)
-   Finally the name
-   So now we have a bunch of concepts to explain

## Permissions in Principle

-   The three A's
    -   [Authentication](g:authentication): who are you
        (or more accurately, what is your identity on this computer system)?
    -   [Authorization](g:authorization): who is allowed to do what?
    -   [Access control](g:access_control): how does the system enforce those rules?
-   So operating systems needs to:
    -   Match a person to an account (we will discuss [elsewhere](../s06_auth/index.md))
    -   Keep track of which account each process belongs to
    -   Keep track of what operations are permitted to whom
    -   Enforce those rules (which we won't go into)

## User and Group IDs

-   Each user account has a unique name and a unique numeric ID
    -   The numeric user ID is often called a [uid](g:uid)
    -   Not to be confused with [UUID](g:uuid)
-   Each user can belong to one or more [groups](g:user_group)
    -   Each of which also has a unique name and a unique group ID (or [gid](g:gid))

```{data-file="id_no_args.sh"}
id
```
```{data-file="id_no_args.out"}
uid=501(tut) gid=20(staff) groups=20(staff),12(everyone),61(localaccounts),…and 15 others…
```

-   Tells us:
    -   User ID is 501 and name is `tut`
    -   Primary group ID is 20 (`staff`)
    -   Also belongs to 12 (`everyone`) and 61 (`localaccounts`)
-   Reports by default on the user associated with the currently-running process
-   Can provide an account name to get details of a particular account

```{data-file="id_nobody.sh"}
id -p nobody
```
```{data-file="id_nobody.out"}
uid	nobody
groups	nobody everyone localaccounts
```

## Capabilities

-   A [capability](g:capability) is something that someone may or may not be able to do to a thing
    -   Which is incredibly vague
-   Files and directories capabilities are shown below

| Name    | Abbreviation | File            | Directory                       |
| ------- | ------------ | --------------- | ------------------------------- |
| Read    | r            | Inspect content | See what the directory contains |
| Write   | w            | Modify content  | Add or remove contents          |
| Execute | x            | Run program     | Enter or pass through directory |

-   Read and write make sense
-   Execute makes sense on files
    -   See below for how the operating system figures out how to run a file
-   Execute on directories is basically "we needed something and this bit was available"
    -   Want to be able to run `dir/program`
    -   *Without* seeing what else is in `dir`
    -   Use the "execute" bit on the directory `dir`

## Permissions in Practice

-   Go back to permissions
-   First letter is `-` for a regular file and `d` for a directory
    -   We will see other things below
-   Then show read-write-execute permissions for user, group, and other (i.e., everyone else)
-   So `drwxr-xr-x` means "a directory with owner=RWX, group=RX, and other=RX"
-   And `-rw-r--r--` means "a file with owner=RW, group=R, and other=R"

## Changing Permissions

-   Change permissions with `chmod` ("change mode")
    -   Unfortunately one of the more confusing Unix shell commands
-   Simplest form: `chmod u=rw,g=r,o=r`
    -   Specify read-write-execute explicitly for user-group-other

```{data-file="chmod_example.text"}
$ echo "original content" > /tmp/somefile.txt

$ ls -l /tmp/somefile.txt
-rw-r--r--  1 gvwilson  staff  17 Apr 20 16:15 /tmp/somefile.txt

$ cat /tmp/somefile.txt
original content

$ chmod u=,g=,o= /tmp/somefile.txt

$ ls -l /tmp/somefile.txt
----------  1 gvwilson  staff  17 Apr 20 16:15 /tmp/somefile.txt

$ cat /tmp/somefile.txt
cat: /tmp/somefile.txt: Permission denied

$ echo "revised content" > /tmp/somefile.txt
src/fs/chmod_example.sh: line 9: /tmp/somefile.txt: Permission denied

$ chmod u=rw /tmp/somefile.txt

$ echo "revised content" > /tmp/somefile.txt

$ ls -l /tmp/somefile.txt
-rw-------  1 gvwilson  staff  16 Apr 20 16:15 /tmp/somefile.txt

$ cat /tmp/somefile.txt
revised content
```

## Changing Permissions Programmatically

-   `ls`, `chmod`, and other programs use [system calls](g:system_call) to get information and change things
    -   A function provided by the operating system
-   Other programs can also use those system calls

```{data-file="chmod_example.py:create"}
import os
import stat

filename = "/tmp/somefile.txt"
with open(filename, "w") as writer:
    writer.write("original content")

status = os.stat(filename)

print(status)
# os.stat_result(st_mode=33188, st_ino=99159112, st_dev=16777234, st_nlink=1, st_uid=501,
#                st_gid=0, st_size=16, st_atime=1713644644, st_mtime=1713644747,
#                st_ctime=1713644747)

print(status.st_mode)
# 33188

print(stat.filemode(status.st_mode))
# -rw-r--r--

print(f"user ID {status.st_uid} group ID {status.st_gid}")
# user ID 501 group ID 0
```

-   `os.stat` returns a tuple with named fields
    -   All start with `st_` prefix because that's what the original C structure did
-   `status.st_mode` doesn't make much sense in decimal
    -   Often printed in [octal](g:octal)
    -   Much easier to use `stat.filemode` to turn it into an `ls`-style string

```{data-file="chmod_example.py:lockdown"}
os.chmod(filename, 0)
status = os.stat(filename)
print(stat.filemode(status.st_mode))
# ----------

try:
    with open(filename, "r") as reader:
        content = reader.read()
except OSError as exc:
    print(f"trying to open and read: {type(exc)} {exc}")
# trying to open and read: <class 'PermissionError'>
# [Errno 13] Permission denied: '/tmp/somefile.txt
```

-   Use `os.chmod` to set the permission to nothing-nothing-nothing (i.e., 0)
-   Trying to read/write file after that causes `PermissionError` (a subclass of `OSError`)
-   `stat` defines constants representing various permissions
-   Add the ones we want

## Not Important Until It Is

-   Permissions are less important on laptops than they were on multi-user systems…
-   …until we start to run web servers and databases that other people can access

## Systems Programming?

-   Not a precise term
-   But if it means anything,
    it includes things at this level

## Hard Links

-   One of the columns in earlier table is "links"
    -   How many references there are to a file in the filesystem
-   Can create more links to an existing file
    -   What we think of as "files" are bookkeeping entries in the filesystem that refer to inodes
-   Use the `ln` command to create a [hard link](g:link_hard)
    -   Syntax is like `mv`: existing first, then new name

```{data-file="hard_link.text"}
$ echo "file content" > /tmp/original.txt

$ ls -l /tmp/*.txt
-rw-r--r--  1 tut  staff  13 Apr 20 20:13 /tmp/original.txt

$ ln /tmp/original.txt /tmp/duplicate.txt
$ ls -l /tmp/*.txt
-rw-r--r--  2 tut  staff  13 Apr 20 20:13 /tmp/duplicate.txt
-rw-r--r--  2 tut  staff  13 Apr 20 20:13 /tmp/original.txt

$ cat /tmp/duplicate.txt
file content

$ rm /tmp/original.txt
$ ls -l /tmp/*.txt
-rw-r--r--  1 tut  staff  13 Apr 20 20:13 /tmp/duplicate.txt

$ cat /tmp/duplicate.txt
file content
```

-   Note the number of links to `original.txt` and `duplicate.txt` is 2 when they both exist

## Symbolic Links

-   A [symbolic link](g:link_sym) (or symlink) is a file that refers to another file

<figure id="fs_links">
  <img src="links.svg" alt="Relationship between hard and symbolic Links"/>
  <figcaption>Figure 1: Hard and Symbolic Links</figcaption>
</figure>

```{data-file="sym_link.text"}
$ echo "file content" > /tmp/original.txt

$ ls -l /tmp/*.txt
-rw-r--r--  1 tut  staff  13 Apr 20 20:20 /tmp/original.txt

$ ln -s /tmp/original.txt /tmp/duplicate.txt
$ ls -l /tmp/*.txt
lrwxr-xr-x  1 tut  staff  17 Apr 20 20:20 /tmp/duplicate.txt -> /tmp/original.txt
-rw-r--r--  1 tut  staff  13 Apr 20 20:20 /tmp/original.txt

$ cat /tmp/duplicate.txt
file content

$ readlink /tmp/duplicate.txt
/tmp/original.txt

$ rm /tmp/original.txt
$ ls -l /tmp/*.txt
lrwxr-xr-x  1 tut  staff  17 Apr 20 20:20 /tmp/duplicate.txt@ -> /tmp/original.txt

$ cat /tmp/duplicate.txt
cat: /tmp/duplicate.txt: No such file or directory
```

-   Soft links can have different permissions
    -   Hard links all refer to the same inode, which is where permissions are stored
-   Often use soft links to hide version numbers of installed applications
    -   E.g., `~/conda/bin/python` is a symlink to `~/conda/bin/python3.11`
    -   Running the former actually launches the latter

## Other Kinds of "Files"

-   Unix (and other modern operating systems) make [devices](g:device) look like files
    -   Reading from the keyboard and writing to the screen are like file I/O
-   The pseudofiles representing devices live in `/dev`
-   `ls /dev` on my machine shows 345 different devices
-   Key difference between different kinds is whether access is [buffered](g:buffer_verb)
    -   Does the operating system read a block at a time and then give the user access to the block?
    -   Does it store data in a block temporarily and write that block all at once?
-   A [character device](g:character_device) allows direct (unbuffered) access
    -   Example: terminals whose names are `/dev/tty*`
    -   `ls -l` shows `c` as the first letter instead of `d` for directory
-   A [block device](g:block_device) always buffers
    -   Example: a disk whose name is `/dev/disk*`
    -   `ls -l` shows `b` instead of `c`, `d`, `l`, or `-`
-   There are stranger things as well
    -   `dev/urandom` produces random bits

```{data-file="random_bits.py"}
with open("/dev/urandom", "rb") as reader:
    bytes = reader.read(8)
print([hex(b) for b in bytes])```

## Disks

-   Run the `df` command (for "disk free space")

```{data-file="df_output.out"}
Filesystem     512-blocks      Used  Available Capacity iused      ifree %iused  Mounted on
/dev/disk3s1s1 1942700360  20008776 1812103064     2%  403755 4294159622    0%   /
devfs                 414       414          0   100%     722          0  100%   /dev
/dev/disk3s6   1942700360        40 1812103064     1%       0 9060515320    0%   /System/Volumes/VM
/dev/disk3s2   1942700360  11963032 1812103064     1%    1069 9060515320    0%   /System/Volumes/Preboot
/dev/disk3s4   1942700360      7664 1812103064     1%      52 9060515320    0%   /System/Volumes/Update
/dev/disk1s2      1024000     12328     984504     2%       1    4922520    0%   /System/Volumes/xarts
/dev/disk1s1      1024000     12544     984504     2%      28    4922520    0%   /System/Volumes/iSCPreboot
/dev/disk1s3      1024000      4904     984504     1%      89    4922520    0%   /System/Volumes/Hardware
/dev/disk3s5   1942700360  96389600 1812103064     6%  955583 9060515320    0%   /System/Volumes/Data
map auto_home           0         0          0   100%       0          0     -   /System/Volumes/Data/home
```

-   The physical disk in this laptop is divided into several filesystems
    -   Each has its own inodes
-   How many 512-byte blocks does each have?
-   How many are used and available?
-   How many inodes are used and available?
-   Where is the filesystem [mounted](g:mount)?
    -   I.e., what path do we use to tell the operating system we want that data?
-   Most people won't ever have to worry about disks at this level
    -   But we *will* think about mounting [elsewhere](../s07_virt/index.md)

## Disk Usage

-   Use the `du` command with `-h` for human-readable suffixes and `-s` for summary

```{data-file="du_h_s.text"}
$ du -h -s .
4.9M	.
```

-   But this doesn't include `.git` or other files and directories whose names start with `.`
-   Simple solution `du -h -s .*` tries to summarize `..`, which isn't what we want
-   Use [command interpolation](g:command_interpolation) and `ls -A`
    -   All of these tools evolved piece by piece over time, and it shows

```{data-file="du_h_s_all.text"}
$ du -h -s $(ls -A)
1.8M	.git
4.0K	.gitignore
4.0K	.vscode
4.0K	CODE_OF_CONDUCT.md
8.0K	CONTRIBUTING.md
8.0K	LICENSE.md
4.0K	Makefile
4.0K	README.md
4.0K	brew.txt
4.0K	config.py
812K	docs
 28K	info
360K	lib
1.1M	old
4.0K	requirements.txt
524K	res
408K	src
4.0K	tmp
```
