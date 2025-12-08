# Shell Variables

## Operating System vs. Shell

-   Operating system (OS) manages your hardware
    -   Provides a set of system calls
        to make different machines look the same to user-level programs
-   Command shell (or just "shell") is a text UI for interacting with the operating system
    -   And with user-level programs
-   There are many different shells for Unix and Windows
    -   [Bash][bash] and [Zsh][zsh] are compatible with the POSIX standard
    -   [Fish][fish] is nicer, but is not
    -   [Nushell][nushell] is even stranger
    -   [PowerShell][powershell] on Windows (and Unix) has a lot of nice features too
-   We use Bash in this tutorial but will discuss Nushell later

## Shell Variables

-   The shell is a program and programs have variables
-   Create or change with <code><em>name</em>=<em>value</em></code>
-   [Shell variable](g:shell_var) stays in the process that created it
    -   E.g., that particular running copy of the shell
-   Use <code>$<em>name</em></code> to get value
    -   `$` prefix because people type file and directory names more often

```{data-file="shell_var_outer.sh"}
WINDOW="neighbor"
echo "outer: window is ${WINDOW}"
bash src/shell_var_inner.sh
```
```{data-file="shell_var_inner.sh"}
echo "inner: window is ${window}"
```
```{data-file="shell_var_outer.out"}
outer: window is neighbor
inner: window is 
```

-   Note: variables usually written in upper case to distinguish them from filenames
    -   So use underscores as separators

<section class="exercise" markdown="1">

## Exercise: Single Quotes

What happens if you modify the scripts shown above
to use single quotes instead of double quotes?

</section>

## Environment Variables

-   [Environment variable](g:env_var) is inherited by new processes
-   Use <code>export <em>name</em>=<em>value</em></code>

```{data-file="env_var_outer.sh"}
WINDOW="neighbor"
export THRESHOLD=0.5
echo "outer: window is ${WINDOW} and threshold is ${THRESHOLD}"
bash src/env_var_inner.sh
```
```{data-file="env_var_inner.sh"}
echo "inner: window is ${window} and threshold is ${threshold}"
```
```{data-file="env_var_outer.out"}
outer: window is neighbor and threshold is 0.5
inner: window is  and threshold is 
```

<section class="exercise" markdown="1">

## Exercise: Setting in Children

If a child process sets shell or environment variables,
are they visible in the parent once the child finishes executing?

</section>

## Environment Variables in Programs

-   Since environment variables are inherited by child processes,
    they are inherited by all programs run from the shell that has them

```{data-file="env_var_py.sh"}
WINDOW="neighbor"
export THRESHOLD=0.5
echo "outer: window is ${WINDOW} and threshold is ${THRESHOLD}"
python src/env_var_py.py
```
```{data-file="env_var_py.py"}
import os

window = os.getenv("WINDOW", default="not set")
threshold = os.getenv("THRESHOLD", default="not set")
print(f"inner: window is {window} and threshold is {threshold}")
```
```{data-file="env_var_py.out"}
outer: window is neighbor and threshold is 0.5
inner: window is not set and threshold is 0.5
```

## Inspecting Variables

-   `set` on its own lists variables
    -   And functions, because yes, you can create those in the shell
    -   But please don't: if you need that, write a Python script
-   `env` shows all environment variables

```{data-file="show_env_vars.sh"}
env | cut -d = -f 1 | sort | head -n 10
```
```{data-file="show_env_vars.out"}
BASH_SILENCE_DEPRECATION_WARNING
CONDA_DEFAULT_ENV
CONDA_EXE
CONDA_PREFIX
CONDA_PREFIX_1
CONDA_PROMPT_MODIFIER
CONDA_PYTHON_EXE
CONDA_SHLVL
EDITOR
GEM_HOME
```

-   Many tools rely on variables to manage configuration
    -   [NVM][nvm] defines 4, [Conda][conda] defines 8
    -   No guarantee that their names don't [%g name_collision "collide" %]

<section class="exercise" markdown="1">

## Exercise: Python vs. the Shell

The `os.environ` variable in Python's `os` module
is an easy way to get all of the process's environment variables.
Compare it to what `env` shows.

1.  Are there differences?

2.  If so, what are they and why do they exist?

</section>

## Important Environment Variables

-   37 environment variables in my current shell
-   Most important are shown in [%t var_common %]

| Name     | Typical Value    | Purpose                           |
| -------- | ---------------- | --------------------------------- |
| `EDITOR` | `nano`           | default text editor               |
| `HOME`   | `/Users/tut`     | user's home directory             |
| `LANG`   | `en_CA.UTF-8`    | user's preferred (human) language |
| `PATH`   | see below        | search path for programs          |
| `PWD`    | `/Users/tut/sys` | present working directory         |
| `SHELL`  | `/bin/bash`      | user's default shell              |
| `TERM`   | `xterm-256color` | type of terminal                  |
| `TMPDIR` | `/var/tmp`       | storage for temporary files       |
| `USER`   | `tut`            | current user's name               |

## Search Path

-   `PATH` holds a colon-separated list of directories
-   Shell looks in these *in order* to find commands
-   Reading at them all on one line is difficult, so use `tr` to split

```{data-file="show_path.sh"}
echo $PATH | tr : '\n'
```
```{data-file="show_path.out"}
/Users/tut/google-cloud-sdk/bin
/Users/tut/conda/envs/sys/bin
/Users/tut/conda/condabin
/Users/tut/.nvm/versions/node/v20.8.0/bin
/Users/tut/bin
/Applications/Postgres.app/Contents/Versions/14/bin
/Users/tut/go/bin
/usr/local/bin
/System/Cryptexes/App/usr/bin
/usr/bin
/bin
/usr/sbin
/sbin
/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin
/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin
/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin
/Library/Apple/usr/bin
/Library/TeX/texbin
/usr/local/bin
```

-   Notice `/Users/tut/bin`
-   Common to have a `~/bin` directory with the user's own utilities

## Adding to the Search Path

-   Shell variables (of both kinds) are just strings
-   So add to search path by redefining the variable
    -   New directory at the from
    -   Entire old value at the back

```{data-file="change_path.sh"}
export PATH="/tmp/bin:${PATH}"
echo $PATH | tr : '\n' | head -n 5
```
```{data-file="change_path.out"}
/tmp/bin
/Users/gregwilson/google-cloud-sdk/bin
/Users/gregwilson/conda/envs/sys/bin
/Users/gregwilson/conda/condabin
/Users/gregwilson/.gem/ruby/3.1.2/bin
```

<section class="exercise" markdown="1">

## Exercise: Shortening the Path

Removing a directory from `PATH` is harder than adding one.
Write a shell script that:

1.  Splits `PATH` on colons to put one entry on each line.
2.  Uses `grep` to remove the undesired line.
3.  Uses `paste -s -d :` to recombine the lines.
4.  Uses command interpolation to assign the result back to `PATH`.

This exercise may remind you why
complicated operations should be done in Python rather than in the shell.

</section>

## Startup Files

-   Bash shell runs commands in `~/.bash_profile` for login shells
-   Bash shell runs commands in `~/.bashrc` for interactive shells
-   Yes, the terminology is confusing
-   Common to have `~/.bash_profile` [%g source_shell "source" %] `~/.bashrc`
    -   I.e., run those commands in the current shell

```{data-file="source_bashrc.sh"}
source $HOME/.bashrc
```

## Command Interpolation {: .aside}

-   Can use <code>outer $(<em>inner</em>)</code> to run `inner` and use its output as arguments to `outer`
-   Long-winded way to count lines in some text files

```{data-file="interpolate.sh"}
wc -l $(ls src/*.text)
```
```{data-file="interpolate.out"}
      12 src/ctrl_z_background.text
      12 src/kill_int.text
       6 src/kill_process.text
      30 total
```
