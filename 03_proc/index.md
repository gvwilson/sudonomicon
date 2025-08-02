# Processes

## Program vs. Process

-   A program is a set of instructions for a computer
-   A [process](g:process) is a running instance of a program
    -   Code plus variables in memory plus open files plus some IDs
-   If files are nouns, processes are verbs
-   Tools to manage processes were invented when most users only had a single terminal
    -   But are still useful for working with remote/cloud machines

## Viewing Processes

-   Use `ps -a -l` to see currently running processes in terminal
    -   `UID`: numeric ID of the user that the process belongs to
    -   `PID`: process's unique ID
    -   `PPID`: ID of the process's parent (i.e., the process that created it)
    -   `CMD`: the command the process is running

```{data-file="ps_a_l.sh"}
ps -a -l
```
```{data-file="ps_a_l.out"}
  UID   PID  PPID        F CPU PRI NI        SZ    RSS       TTY       TIME CMD
    0 13215 83470     4106   0  31  0 408655632   9504   ttys001    0:00.02 login -pfl gvwilson /
  501 13216 13215     4006   0  31  0 408795632   5424   ttys001    0:00.04 -bash
  501 13569 13216     4046   0  31  0 408895008  20864   ttys001    0:00.10 python -m http.server
    0 13577 13216     4106   0  31  0 408766128   1888   ttys001    0:00.01 ps -a -l
```

-   Use `ps -a -x` to see (almost) all processes running on computer
    -   `ps -a -x | wc` tells me there are 655 processes running on my laptop right now

## Exercise {: .exercise}

1.  What does the `top` command do?
    What does `top -o cpu` do?

1.  What does the `pgrep` command do?

## Parent and Child Processes

-   Every process is created by another process
    -   Except the first, which is started automatically when the operating system boots up
-   Refer to [child process](g:child_process) and [parent process](g:parent_process)
-   `echo $$` shows [process ID](g:process_id) of current process
    -   `$$` shortcut for current process's ID because it's used so often
-   `echo $PPID` (parent process ID) to get parent
-   `pstree $$` to see [process tree](g:process_tree)

## Signals

-   Can send a [signal](g:signal) to a process
    -   "Something extraordinary happened, please deal with it immediately"
-   Table shows what happened

| Number | Name      | Default Action    | Description |
| -----: | --------- | ----------------- | ----------- |
|      1 | `SIGHUP`  | terminate process | terminal line hangup |
|      2 | `SIGINT`  | terminate process | interrupt program |
|      3 | `SIGQUIT` | create core image | quit program |
|      4 | `SIGILL`  | create core image | illegal instruction |
|      8 | `SIGFPE`  | create core image | floating-point exception |
|      9 | `SIGKILL` | terminate process | kill program |
|     11 | `SIGSEGV` | create core image | segmentation violation |
|     12 | `SIGSYS`  | create core image | non-existent system call invoked |
|     14 | `SIGALRM` | terminate process | real-time timer expired |
|     15 | `SIGTERM` | terminate process | software termination signal |
|     17 | `SIGSTOP` | stop process      | stop (cannot be caught or ignored) |
|     24 | `SIGXCPU` | terminate process | CPU time limit exceeded |
|     25 | `SIGXFSZ` | terminate process | file size limit exceeded |

-   Create a [callback function](g:callback_function)
    to act as a [signal handler](g:signal_handler)

```{data-file="catch_interrupt.py"}
import signal
import sys

COUNT = 0

def handler(sig, frame):
    global COUNT
    COUNT += 1
    print(f"interrupt {COUNT}")
    if COUNT >= 3:
        sys.exit(0)

signal.signal(signal.SIGINT, handler)
print("use Ctrl-C three times")
while True:
    signal.pause()
```
```{data-file="catch_interrupt.out"}
python src/catch_interrupt.py
use Ctrl-C three times
^Cinterrupt 1
^Cinterrupt 2
^Cinterrupt 3
```

-   `^C` shows where user typed Ctrl-C

## Background Processes

-   Can run a process in the [background](g:background_process)
    -   Only difference is that it isn't connected to the keyboard (stdin)
    -   Can still print to the screen (stdout and stderr)

```{data-file="show_timer.py"}
import time

for i in range(3):
    print(f"loop {i}")
    time.sleep(1)
print("loop finished")
```
```{data-file="show_timer.sh"}
python src/show_timer.py &
ls site
```
```{data-file="show_timer.out"}
$ src/show_timer.sh
birds.csv		cert_authority.srl	sandbox			server.pem		species.csv
cert_authority.key	motto.json		server.csr		server_first_cert.pem	yukon.db
cert_authority.pem	motto.txt		server.key		server_first_key.pem
loop 0
$ loop 1
loop 2
loop finished
```

-   `&` at end of command means "run in the background"
-   So `ls` command executes immediately
-   But `show_timer.py` keeps running until it finishes
    -   Or needs keyboard input
-   Can also start process and then [suspend](g:suspend_process) it with Ctrl-Z
    -   Sends `SIGSTOP` instead of `SIGINT`
-   Use `jobs` to see all suspended processes
-   Then <code>bg %<em>num</em></code> to resume in the background
-   Or <code>fg %<em>num</em></code> to [foreground](g:foreground_process) the process
    to [resume](g:resume_process) its execution

```{data-file="ctrl_z_background.text"}
$ python src/show_timer.py
loop 0
^Z
[1]+  Stopped                 python src/show_timer.py
$ jobs
[1]+  Stopped                 python src/show_timer.py
$ bg
[1]+ python src/show_timer.py &
loop 1
$ loop 2
loop finished
[1]+  Done                    python src/show_timer.py
```

-   Note that input and output are mixed together

## Killing Processes

-   Use `kill` to send a signal to a process

```{data-file="kill_process.text"}
$ python src/show_timer.py
loop 0
^Z
[1]+  Stopped                 python src/show_timer.py
$ kill %1
[1]+  Terminated: 15          python src/show_timer.py
```

-   By default, `kill` sends `SIGTERM` (terminate process)
-   Variations:
    -   Give a process ID: `kill 1234`
    -   Send a different signal: `kill -s INT %1`

```{data-file="kill_int.text"}
$ python src/show_timer.py
loop 0
^Z
[1]+  Stopped                 python src/show_timer.py
$ kill -s INT %1
[1]+  Stopped                 python src/show_timer.py
$ fg
python src/show_timer.py
Traceback (most recent call last):
  File "/tut/sys/src/show_timer.py", line 5, in <module>
    time.sleep(1)
KeyboardInterrupt
```

## Fork

-   [Fork](g:fork_process) creates a duplicate of a process
    -   Creator is parent, gets process ID of child as return value
    -   Child gets 0 as return value (but has something else as its process ID)

```{data-file="fork.py"}
import os

print(f"starting {os.getpid()}")
pid = os.fork()
if pid == 0:
    print(f"child got {pid} is {os.getpid()}")
else:
    print(f"parent got {pid} is {os.getpid()}")
```
```{data-file="fork.out"}
starting 41618
parent got 41619 is 41618
child got 0 is 41619
```

## Unpredictability {: .aside}

-   Output shown above comes from running the program interactively
-   When run as `python fork.py > temp.out`, the "starting" line may be duplicated
    -   Programs don't write directly to the screen
    -   Instead, they send text to the operating system for display
    -   The operating system buffers output (and input)
    -   So the "starting" message may be sitting in a buffer when `fork` happens
    -   In which case both parent and child send it to the operating system to print
-   OS decides how much to buffer and when to actually display it
-   Its decision can be affected by what else it is doing
-   So running the same program several times can produce different outputs
    -   Because your program is only part of a larger sequence of operations
-   Dealing with issues like these is
    part of what distinguishes systems programming from "regular" programming

## Flushing I/O

-   Can force OS to do I/O *right now* by [flushing](g:flush) its buffers

```{data-file="flush.py"}
import os
import sys

print(f"starting {os.getpid()}")
sys.stdout.flush()
pid = os.fork()
if pid == 0:
    print(f"child got {pid} is {os.getpid()}")
else:
    print(f"parent got {pid} is {os.getpid()}")
```
```{data-file="flush.out"}
starting 41536
parent got 41537 is 41536
child got 0 is 41537
```

## Exec

-   The `exec` family of functions in `os` execute a new program
    *inside the calling process*
    -   Replace existing program and start a new one
    -   One of the reasons we need to distinguish "process" from "program"
-   Use `fork`/`exec` to create a new process and then run a program in it

```{data-file="fork_exec.py"}
import os
import sys

print(f"starting {os.getpid()}")
sys.stdout.flush()
pid = os.fork()
if pid == 0:
    os.execl("/bin/echo", "echo", f"child echoing {pid} from {os.getpid()}")
else:
    print(f"parent got {pid} is {os.getpid()}")
```
```{data-file="fork_exec.out"}
starting 46713
parent got 46714 is 46713
child echoing 0 from 46714
```

## Exercise {: .exercise}

1.  What are the differences between `os.execl`, `os.execlp`, and `os.execv`?
    When and why would you use each?
