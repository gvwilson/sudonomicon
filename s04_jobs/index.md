# Running Jobs

-   Computers don't get bored, so get them to do boring things

## Watching a Command

-   The `watch` command runs a command periodically and displays result
    -   Hard to show output statically…

```{data-file="watch_date.text"}
$ watch -n 5 date
Every 5.0s: date              cherne: Mon Apr 22 16:11:48 2024

Mon Apr 22 16:11:53 EDT 2024
```

-   `-n 5`: every five seconds
-   Less distracting to show without title (`-t`)

```{data-file="watch_date_no_title.text"}
$ watch -t -n 5 date
Mon Apr 22 16:11:53 EDT 2024
```

-   More useful to show differences with `-d`
-   Each successive update highlights the difference from the previous one
    -   Again, hard to show statically
-   Also use to use `-g` to exit when the command's output changes
-   E.g., `watch -n 1 -g netstat` will exit within one second of network activity

## Watching Files

-   Use `fswatch` (file system watch)

```{data-file="fswatch_example.text"}
$ fswatch -l 1 -x Created -x Removed /tmp

# touch /tmp/a.txt
/private/tmp/a.txt Created IsFile

# rm /tmp/a.txt
/private/tmp/a.txt Created IsFile Removed
```

-   `-l 1`: latency of one second (i.e., how often to report)
-   `-x Created -x Removed`: what events to watch for
-   `/tmp`: look for any changes in this directory
-   Get one line per change
    -   Common to pipe the output of `fswatch` to something that parses these lines and acts on them
-   FIXME: why does removing the file generate a 'Created' record?

## And Then There's `cron`

-   `cron` runs jobs at specified times
-   Which sounds simple, but its interface is complex even by Unix standards
    -   And differences between different machines make life even harder
-   Most research programmers won't ever need it
-   If you do, consult [crontab.guru][crontab-guru]

## Git Hooks

-   Git stores repository data in `.git`
-   Contains a directory called `hooks`
-   Git automatically runs programs it finds there at particular times
    -   E.g., if there is a program called `pre-commit`, Git runs it before each commit takes place
-   What happens next depends on the program's exit [exit status](g:exit_status)
    -   0: no problems
    -   anything else: an error code of some sort

```{data-file="pre_commit_always_fail.text"}
# Make a place for this example.
$ mkdir example
$ cd example

# Turn it into a Git repository.
$ git init .
Initialized empty Git repository in /Users/tut/example/.git/

# Create a pre-commit script that always fails (i.e., exits with non-zero status).
$ cat > .git/hooks/pre-commit.sh
#!/bin/sh
echo "hook running"
exit 1

# Make that script executable.
$ chmod 755 .git/hooks/pre-commit.sh

# Run it and check its exit status.
$ .git/hooks/pre-commit.sh
hook running

$ echo $?
1

# Create some content.
$ cat > a.txt
content

# Try committing it.
# The hook should print "hook running" and the commit should be prevented.
$ git add a.txt

$ git commit -m "should not work"
hook running

$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   a.txt
```

-   More useful to check the files or something else

```{data-file="pre_commit_ruff.text"}
$ cat > .git/hooks/pre-commit
ruff check
exit $?

$ cat > a.py
x = not_defined

$ git add .
$ git commit
a.py:1:5: F821 Undefined name `not_defined`
Found 1 error.

$ cat > a.py
x = 0

$ git add .
$ git commit -m "this commit works"
All checks passed!
[main 7c01aee] this commit works
 1 file changed, 1 insertion(+), 1 deletion(-)
```

-   Use [ruff][ruff] to [lint](g:lint) the project's Python code
-   Exit with whatever exit status it returned
    -   `$?` is the exit status of the most recently run process in the shell

## Managing These Examples {: .aside}

-   Want to include the examples shown above in this repository and re-run them automatically
-   But nesting Git repositories is tricky
-   And re-running these commands *and* capturing all their output is also hard
