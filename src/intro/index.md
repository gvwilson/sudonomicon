---
title: "Introduction"
syllabus:
- fixme
---

## What This Is {: .aside}

-   Notes and working examples that instructors can use to perform a lesson
    -   Do *not* expect novices with no prior Unix experience to be able to learn from them on their own
-   Musical analogy
    -   This is the chord changes and melody
    -   We expect instructors to create an arrangement and/or improvise while delivering
-   Please see [the license](./license/) for terms of use,
    the [Code of Conduct](./conduct/) for community standards,
    and [these guidelines](./contributing/) for notes on contributing
-   [Greg Wilson][wilson_greg] is a programmer, author, and educator based in Toronto

## Scope {: .aside}

-   [Intended audience][persona]
    -   Ning did a bachelor's degree in economics
        and now works as a data analyst for the Ministry of Health
    -   They are comfortable working with Unix command-line tools,
        writing data analysis programs in Python,
	and downloading data from the web manually
    -   Ning wants to understand what happens when they install a package
	or run a pipeline in the cloud
    -   Their work schedule is unpredictable and highly variable,
        so they need to be able to learn a bit at a time
-   Prerequisites
    -   Unix shell commands covered in [this Software Carpentry lesson][sc_shell]:
        -   `pwd`; `ls`; `cd`; `.` and `..`; `rm` and `rmdir`; `mkdir`; `touch`;
            `mv`; `cp`; `tree`; `cat`; `wc`; `head`; `tail`; `less`; `cut`; `echo`;
            `history`; `find`; `grep`; `zip`; `man`
        -   current working directory; absolute and relative paths; naming files;
            editing with `nano`
        -   standard input; standard output; standard error; redirection; pipes
        -   `*` and `?` wildcards; shell variable with `$` expansion; `for` loop
    -   Python for command-line scripting
        -   variables; numbers and strings; lists; dictionaries; `for` and `while` loops;
	    `if`/`else`; `with`; defining and calling functions; `sys.argv`, `sys.stdin`,
	    and `sys.stdout`; simple regular expressions; reading JSON data;
	    reading CSV files using [Pandas][pandas] or [Polars][polars]
        -   `pip install`
	-   `python -m venv` or `conda create`
-   Learning outcomes
    1.  Explain the difference between shell variables and environment variables
        and write shell scripts that use each.
    1.  Create a virtual environment and explain what this actually does.
    1.  Create `requirements.txt` file for [`pip`][pip] and explain version pinning.
    1.  Explain what a filesystem is (disk partitions, inodes, symbolic links)
        and use `df`, `ln`, similar commands to explore with them.
    1.  Explain what a process is and use commands like `ps` and `kill` to explore and manage them.
    1.  Explain what a job is and use commands like `jobs`, `bg`, and `fg` to manage them.
    1.  Explain what `cron` jobs are and how to create them.
    1.  Explain the difference between a container and a virtual machine.
    1.  Create and manage Docker images.
    1.  Explain what ports are and write Python code that uses sockets and HTTP.
    1.  Explain what certificates are and how they are used to support HTTPS.
    1.  Explain what key pairs are and how they are stored, and create and manage key pairs.
    1.  Explain what IP addresses are and how they are resolved.
    1.  Explain how traditional password authentication works and describe its weaknesses.

## Setup {: .aside}

-   Download [the latest release]([% config "release" %])
-   Unzip the file in a temporary directory to create:
    -   `./site/*.*`: files and directories used in examples
    -   `./src/*.*`: shell scripts and Python programs
    -   `./out/*.*`: expected output for examples

## Acknowledgments {: .aside}

My thanks to everyone who helped make this tutorial possible:

[% thanks %]
