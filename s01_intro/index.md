# Introduction

## Objective

-   Tried teaching computer security to data scientists
-   Had to back up every few minutes to explain underlying concepts
    -   "What does it mean to 'mount' a filesystem?"
    -   "What does it mean to 'background' a job?"
    -   "What is a 'port'?"
-   Answer those questions step-by-step so that securing a web service will make sense

## What This Is

-   Notes and working examples that instructors can use to perform a lesson
-   Musical analogy
    -   This is the chord changes and melody
    -   We expect instructors to create an arrangement and/or improvise while delivering
-   Please see [the license](../LICENSE.md) for terms of use,
    the [Code of Conduct](../CODE_OF_CONDUCT.md) for community standards,
    and [these guidelines](../CONTRIBUTING.md) for notes on contributing

## Scope

-   Intended audience
    -   Ning did a bachelor's degree in economics
        and now works as a data analyst for the Ministry of Health
    -   They are comfortable working with common Unix command-line tools,
        writing data analysis scripts in Python,
	and downloading data from the web manually
    -   They want to understand what happens when they install a package
	or run a pipeline in the cloud
    -   Their work schedule is unpredictable and highly variable,
        so they need to be able to learn a bit at a time

## Prerequisites

-   Unix shell commands covered in [this Software Carpentry lesson][sc_shell]:
    -   `pwd`; `ls`; `cd`; `.` and `..`; `rm` and `rmdir`; `mkdir`; `touch`;
        `mv`; `cp`; `tree`; `cat`; `wc`; `head`; `tail`; `less`; `cut`; `echo`;
        `history`; `find`; `grep`; `zip`; `man`
    -   current working directory; absolute and relative paths; naming files
    -   standard input; standard output; standard error; redirection; pipes
    -   `*` and `?` wildcards; shell variable with `$` expansion; `for` loop
-   Python for command-line scripting
    -   variables; numbers and strings; lists; dictionaries; `for` and `while` loops;
        `if`/`else`; `with`; defining and calling functions; `sys.argv`, `sys.stdin`,
        and `sys.stdout`; simple regular expressions; reading JSON data;
        reading CSV files using [Pandas][pandas] or [Polars][polars]
    -   create an environment with [uv][uv]; activate it and install packages

## Learning Outcomes

1.  Explain what environment variables are and write programs that use them.
1.  Create a virtual environment and explain what this actually does.
1.  Create `requirements.txt` file for Python and explain version pinning.
1.  Explain what a filesystem is (disk partitions, inodes, symbolic links)
    and use `df`, `ln`, similar commands to explore with them.
1.  Explain what a process is and use commands like `ps` and `kill` to explore and manage them.
1.  Explain what a job is and use commands like `jobs`, `bg`, and `fg` to manage them.
1.  Explain what `cron` jobs are and how to create them.
1.  Explain the difference between a container and a virtual machine.
1.  Create and manage [Docker][docker] images.
1.  Explain what ports are and write Python code that uses sockets and HTTP.
1.  Explain what certificates are and how they are used to support HTTPS.
1.  Explain what key pairs are and how they are stored, and create and manage key pairs.
1.  Explain what IP addresses are and how they are resolved.
1.  Explain how traditional password authentication works and describe its weaknesses.

## Setup

-   Download the latest release
-   Unzip the file in a temporary directory to create:
    -   `./site/*.*`: files and directories used in examples
    -   `./src/*.*`: shell scripts and Python programs
    -   `./out/*.*`: expected output for examples
