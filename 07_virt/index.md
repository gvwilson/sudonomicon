# Virtualization

-   See [[Stoneman2020](b:Stoneman2020)]

## Virtual Environments

-   If two directories `A` and `B` contain a program `xyz`
    and `A` comes before `B` in the user's `PATH`,
    the command `xyz` will run `A/xyz` instead of `B/xyz`
-   This is how [virtual environments](g:virtual_env) work

```{data-file="show_virtual_env.sh"}
echo $PATH | tr : '\n' | grep conda
echo "python is" $(which python)

```
```{data-file="show_virtual_env.out"}
/Users/tut/conda/envs/sys/bin
/Users/tut/conda/condabin
python is /Users/tut/conda/envs/sys/bin/python
```

-   Virtual environment is initially a minimal Python installation
-   Installing new packages puts them in the environment's directory

## Package Installation

1.  Create a new virtual environment called `example`: `conda create -n example python=3.12`
2.  Activate that virtual environment: `conda activate example`
3.  Install the `faker` package: `pip install faker`

```{data-file="find_faker.sh"}
find $HOME/conda/envs/example -name faker
```
```{data-file="find_faker.out"}
/Users/tut/conda/envs/example/bin/faker
/Users/tut/conda/envs/example/lib/python3.12/site-packages/faker
```

-   The script in `bin` loads the module and runs it

```{data-file="faker_bin.py"}
#!/Users/gvwilson/conda/envs/example/bin/python3.12
# -*- coding: utf-8 -*-
import re
import sys
from faker.cli import execute_from_command_line
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(execute_from_command_line())
```

-   The directory under `site-packages` has 642 Python files (as of version 24.3.0)
-   The `python` in the virtual environment' `bin` directory
    knows to look in that environment's `site-packages` directory

## Exercises {: .exercise}

What is the `re.sub` call in the `faker` script doing and why?

## Limits of Virtual Environments {: .aside}

-   `conda` (and equivalents like `python -m venv`) work for Python
-   But what if you need an isolated environment for several languages at once?
    -   Rust, JavaScript, and other languages all have their own solutions
-   And what if you want other people to be able to reproduce that environment?

## Docker

-   [Docker][docker] solves these problems (and others)
-   Define an [image](g:docker_image) with its own copy of the operating system, filesystem, etc.
-   Run it in a [container](g:docker_container) that is isolated from the rest of your computer

```{data-file="docker_image_ls.sh"}
docker image ls
```
```{data-file="docker_image_ls.out"}
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
```
```{data-file="docker_container_ls.sh"}
docker container ls
```
```{data-file="docker_container_ls.out"}
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

-   Because we haven't created or run anything yet

## Common Error Message {: .aside}

-   Docker requires a [daemon](g:daemon) process
    to be running in the background to start images

```{data-file="docker_image_ls.sh"}
docker image ls
```
```{data-file="docker_image_ls_err.out"}
Cannot connect to the Docker daemon at unix:///Users/tut/.docker/run/docker.sock.
Is the docker daemon running?
```

## Running a Container

```{data-file="docker_run_fresh.text"}
$ docker container run ubuntu:latest
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
bccd10f490ab: Pull complete 
Digest: sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e
Status: Downloaded newer image for ubuntu:latest

$ docker container ls

$ docker container ls -a
CONTAINER ID   IMAGE           COMMAND       CREATED          STATUS                     PORTS     NAMES
741bb295734f   ubuntu:latest   "/bin/bash"   10 seconds ago   Exited (0) 9 seconds ago             xenodochial_mclaren

$ docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       latest    ca2b0f26964c   3 weeks ago   77.9MB
```

-   Ask Docker to run a container with `ubuntu:latest`
    -   I.e., latest stable version of Ubuntu Linux from [Docker Hub][docker_hub]
-   Docker can't find a [cached](g:cache) copy locally, so it downloads the image
-   Then runs it
-   But its default command is `/bin/bash` with no inputs, so it exits immediately.

## Re-running a Container

```{data-file="docker_run_again.text"}
$ docker container run ubuntu:latest pwd
/

$ docker container run ubuntu:latest ls
bin
boot
dev
…more entries…
usr
var
```

-   Docker doesn't need to download the image again (it's cached)
-   Runs the given command instead of the default `/bin/bash`

## This Doesn't Work {: .aside}

```{data-file="docker_run_error.text"}
$ docker container run ubuntu:latest "echo hello"
docker: Error response from daemon: \
failed to create task for container: \
failed to create shim task: \
OCI runtime create failed: \
runc create failed: \
unable to start container process: \
exec: "echo hello": executable file not found in $PATH: unknown.
```

-   There is no executable in the image's search path called `echo hello` (all one word)

## Pulling Images {: .aside}

-   We don't have to run immediately

```{data-file="docker_pull.text"}
$ docker pull ubuntu:latest
latest: Pulling from library/ubuntu
Digest: sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e
Status: Image is up to date for ubuntu:latest
docker.io/library/ubuntu:latest
```

## What Have We Got?

```{data-file="os_release.text"}
$ docker container run ubuntu cat /etc/os-release
PRETTY_NAME="Ubuntu 22.04.4 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.4 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
```

-   Don't need `:latest` every time (defaults)

## Labels Can Change {: .aside}

-   Image creators can re-use labels
    -   So `ubuntu:latest` can mean something different the next time you refer to it
    -   Which makes a mess of reproducibility
-   But each layer in an image can also be identified by a [hash](g:hash) of its contents
-   So we can reproduce an image exactly when we want to

## Wait, What's a Layer? {: .aside}

-   Every image consists of one or more [layers](g:docker_layer)
-   Upper layers mask things in lower layers
-   So if several images are built on top of `ubuntu:latest` the computer doesn't need to store multiple copies of it
-   Layers are implemented by [copy on write](g:copy_on_write)
    -   When a container writes to memory or disk,
        the operating system stops,
	makes a copy of that part of memory or disk for that container's private use,
	and then continues

<figure id="virt_docker_layers">
  <img src="docker_layers.svg" alt="How layers and copy-on-write work in Docker"/>
  <figcaption>Figure 1: Docker Layers and Copy-on-Write</figcaption>
</figure>

## Inside the Container

```{data-file="docker_run_interactive.text"}
$ docker container run -i -t ubuntu
root@4238b3b51abd:/# pwd
/
root@4238b3b51abd:/# whoami
root
root@4238b3b51abd:/# ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@4238b3b51abd:/# exit
exit
$
```

-   `-i`: interactive
-   `-t`: terminal (kind of)
    -   Combination often abbreviated `-it`
-   The hexadecimal number after `root@` is the container's unique ID

## Persistence

```{data-file="docker_run_nonpersistent.text"}
$ docker container run -i -t ubuntu
root@a8ea570a84d3:/# ls /tmp
root@a8ea570a84d3:/# touch /tmp/proof-we-were-here.txt
root@a8ea570a84d3:/# ls /tmp
proof-we-were-here.txt
root@a8ea570a84d3:/# exit
exit

$ docker container run -i -t ubuntu
root@f792c15ebb5b:/# ls /tmp
root@f792c15ebb5b:/# exit
exit
```

-   Container starts fresh each time it runs
-   Notice that the container's ID changes each time it runs

## What Is Running

```{data-file="docker_container_ls_id.text"}
$ docker container ls --format "table {{.ID}}\t{{.Status}}" |
CONTAINER ID   STATUS                                       |
                                                            |
                                                            | $ docker container run -it ubuntu
                                                            | root@a5427ccdeb26:/#
                                                            |
$ docker container ls --format "table {{.ID}}\t{{.Status}}" |
CONTAINER ID   STATUS                                       |
a5427ccdeb26   Up 38 seconds                                |
                                                            |
                                                            | root@a5427ccdeb26:/# exit
                                                            | exit
                                                            |
$ docker container ls --format "table {{.ID}}\t{{.Status}}" |
CONTAINER ID   STATUS                                       |
```

-   `docker container ls` on its own shows a wide table
-   The command uses [Go][golang] format strings for output
    -   Yes, really…

## IDs Only

```{data-file="docker_container_ids_only.text"}
$ docker container ls -a -q
22b7c4109157
8640cfb5e07a
4c1ffdcb1c88
37f30320bc8b
fa9f02841fe9
```

-   `-a`: all
-   `-q`: quiet
-   So `docker container rm  -f $(docker container ls -a -q)` gets rid of everything

## Filtering

```{data-file="docker_image_ls_filter.text"}
$ docker image ls --filter reference="ubuntu"
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       latest    2b7cc08dcdbb   6 weeks ago   69.2MB
```

-   There are a *lot* of Docker commands…

## Installing Software

-   Use [apt][apt] (Advanced Package Tool)

```{data-file="docker_install_python.text"}
$ docker container run -it ubuntu

# apt update
…lots of output…

# apt install -y python3
…lots of output…

# which python

# which python3
/usr/bin/python3

# python3 --version
Python 3.10.12
```

-   `apt update` to update available package lists
-   `apt install -y` to install the desired package
    -   `-y` to answer "yes" to prompts
    -   Installs lots of dependencies as well
-   Doesn't create `python` (note lack of output)
-   Creates `python3` instead
-   Version is most recent in the default repository
-   But *it isn't there the next time we run*

```{data-file="docker_install_python_nonpersistent.text"}
# exit
exit

$ docker run -it ubuntu

# which python

# exit
exit
```

## Actually Installing Software

-   Create a [Dockerfile](g:dockerfile)
    -   Usually called that and in a directory of its own
    -   Ours is `ubuntu-python3/Dockerfile`

```{data-file="ubuntu-python3/Dockerfile"}
FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y
```

-   Tell docker to build the image

```{data-file="ubuntu_python3_build.text"}
$ docker build -t gvwilson/ubuntu-python3 ubuntu-python3

#0 building with "desktop-linux" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 99B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/ubuntu:latest
#2 DONE 1.6s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [1/3] FROM docker.io/library/ubuntu:latest@sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e
#4 resolve docker.io/library/ubuntu:latest@sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e done
#4 DONE 0.0s

#5 [2/3] RUN apt update
#5 CACHED

#6 [3/3] RUN apt install python3 -y
#6 CACHED

#7 exporting to image
#7 exporting layers done
#7 writing image sha256:c06d47d8275d4ef724dad192bf72daaac6b86701a1be40e1ac03f53092201d71 done
#7 naming to docker.io/gvwilson/ubuntu-python3 done
#7 DONE 0.0s
```

-   Use `-t gvwilson/python3` to [docker_tag](g:g %] the image

```{data-file="ubuntu_python3_run.text"}
$ docker container run -it gvwilson/ubuntu-python3
# which python3
/usr/bin/python3
```

## Inspecting Containers

```{data-file="ubuntu_python3_inspect.text"}
$ docker container inspect 56d9f83286f9
…199 lines of JSON…
```

## Layers

```{data-file="docker_image_history.text"}
$ docker image history gvwilson/ubuntu-python3
IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
c06d47d8275d   24 hours ago   RUN /bin/sh -c apt install python3 -y # buil…   29.5MB    buildkit.dockerfile.v0
<missing>      24 hours ago   RUN /bin/sh -c apt update # buildkit            45.6MB    buildkit.dockerfile.v0
<missing>      3 weeks ago    /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>      3 weeks ago    /bin/sh -c #(nop) ADD file:07cdbabf782942af0…   69.2MB
<missing>      3 weeks ago    /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
<missing>      3 weeks ago    /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
<missing>      3 weeks ago    /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B
<missing>      3 weeks ago    /bin/sh -c #(nop)  ARG RELEASE                  0B
```

-   Docker images are built in [layers](g:docker_layer)
-   Layers can be shared between images to reduce disk space

```{data-file="docker_system_df.text"}
$ docker system df
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          1         1         144.8MB   0B (0%)
Containers      1         0         14B       14B (100%)
Local Volumes   1         0         0B        0B
Build Cache     5         0         62B       62B
```

-   First line (`Images`) shows actual disk space
-   The name `df` comes from a Unix command with that name to show free disk space

## Choosing a Command

-   Add `CMD` with a list of arguments to specify default command to execute when image runs

```{data-file="python3-version/Dockerfile"}
FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y

CMD ["python3", "--version"]
```

-   Build

```{data-file="python3_version_build.text"}
$ docker build -t gvwilson/python3 python3-version
…lots of output…
```

-   Run

```{data-file="python3_version_run.text"}
$ docker container run gvwilson/python3-version
Python 3.10.12
```

-   But that's all we get, because all we asked for was the version
-   So build a new image `gvwilson/python3-interactive` with this Dockerfile
    -   Use `-i` to put Python in interactive mode

```{data-file="python3-interactive/Dockerfile"}
FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y

CMD ["python3", "-i"]
```

-   Run it like this
    -   Use `-it` to connect standard input and output to container when it runs

```{data-file="python3_interactive_run.text"}
$ docker container run -it gvwilson/python3-interactive
Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print("hello")
hello
>>> exit()
$ 
```

## Copying Files Into Images

-   Create a new directory `python3-script` and add this file

```{data-file="python3-script/proof.py"}
print("proof that the script was copied")
```

-   Modify the Docker file to copy it into the image

```{data-file="python3-script/Dockerfile"}
FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y

COPY proof.py /home

CMD ["python3", "/home/proof.py"]
```

-   Build and run

```{data-file="python3_script_run.text"}
$ docker build -t gvwilson/python3-script python3-script
…output…

$ docker container run gvwilson/python3-script
proof that the script was copied
```

## Order Matters {: .aside}

-   `docker build` executes Dockerfile commands in order
-   Caches each layer
-   So put things that change more frequently (like your scripts)
    *after* things that change less frequently (like Linux and Python)

## Exericse {: .exercise}

1.  Create a Dockerfile that installs Git
    and uses it to clone a repository containing a Python script
    as the image is being built,
    then runs that Python script by default.

1.  What is the difference between `CMD` and `ENTRYPOINT` in Dockerfiles?
    When would you use the latter instead of the former?

## Sharing Files

-   Containers exist to provide isolation…
-   …but sometimes we *want* interaction with external resources

```{data-file="mount_temp.text"}
$ mkdir -p /tmp/mount_example

$ echo "proof that mounting works" > /tmp/mount_example/test.txt

$ docker container run -it --mount type=bind,source=/tmp/mount_example,target=/example ubuntu

# ls /example
test.txt

# cat /example/test.txt
proof that mounting works

# cp /example/test.txt /example/copied.txt

# exit

$ ls /tmp/mount_example/
copied.txt	test.txt
```

-   Mounting a storage device makes its contents available at some location in the filesystem
-   Use `--mount` to tell Docker to make a directory of the host filesystem available
    inside the container
    -   `type=bind`: there are other options (e.g., `type=volume`)
    -   `source=/tmp/mount_example`: host filesystem
    -   `target=/example`: where the directory appears in the container

## Environment Variables

-   Do *not* put passwords in Dockerfiles
-   Common instead to pass them via environment variables
    -   Which can also be used for things like server addresses
-   Build this image

```{data-file="ubuntu-env-var-fails/Dockerfile"}
FROM ubuntu:latest

CMD ["echo", "variable is '${ECHO_VAR}'"]
```

-   Run it

```{data-file="ubuntu_env_var_fails.text"}
$ ECHO_VAR=some_string docker container run gvwilson/ubuntu-env-var
variable is '${ECHO_VAR}'
```

-   `CMD` takes the string literally
-   So try this:

```{data-file="ubuntu-env-var-succeeds/show_var.sh"}
#!/usr/bin/env bash
echo "variable is '${ECHO_VAR}'"
```
```{data-file="ubuntu-env-var-succeeds/Dockerfile"}
FROM ubuntu:latest

COPY show_var.sh /home
CMD ["/home/show_var.sh"]
```
```{data-file="ubuntu_env_var_succeeds.text"}
$ docker container run gvwilson/ubuntu-env-var-succeeds
variable is ''

$ ECHO_VAR='it worked' docker container run gvwilson/ubuntu-env-var-succeeds
variable is ''

$ ECHO_VAR='it worked' docker container run -e ECHO_VAR gvwilson/ubuntu-env-var-succeeds
variable is 'it worked'
```

-   First time: not setting the variable
-   Second time: not telling Docker to pass that environment variable to the container
-   Third time: got it right

## Environment Files

-   Often define environment variables in a file and tell Docker to use that
    -   Which means you now have to figure out how to manage a file full of secrets…

```{data-file="set_echo_var.env"}
ECHO_VAR=this is set in a .env file
```
```{data-file="run_with_env_file.text"}
$ docker container run --env-file ./set_echo_var.env gvwilson/ubuntu-env-var-succeeds
variable is 'this is set in a .env file'
```

-   Note the lack of quotes around the variable definition in the `.env` file

## Long-Running Containers

```{data-file="docker_exited.text"}
docker container ls -a --format "table {{.ID}}\t{{.Status}}" | head -n 5
CONTAINER ID   STATUS
56d9f83286f9   Exited (0) 3 minutes ago
3a48286cb202   Exited (0) 7 minutes ago
24e164d06d47   Exited (0) 5 hours ago
6e44181432fd   Exited (0) 5 hours ago
```

-   Container only runs as long as its starting process runs
-   But container itself sticks around until removed

## Long-Lived Service

-   Print a count and the time every second
    -   The `expr` command is rather useful

```{data-file="count-time/count_time.sh"}
#!/usr/bin/env bash
COUNTER=1
while true
do
    echo $COUNTER $(date "+%H:%M:%S")
    COUNTER=$(expr $COUNTER + 1)
    sleep 1
done
```

-   Create a Dockerfile

```{data-file="count-time/Dockerfile"}
FROM ubuntu:latest

COPY count_time.sh /home
CMD ["/home/count_time.sh"]
```

-   Build and run as usual

```{data-file="count_time_first.text"}
$ docker container run gvwilson/count-time
1 18:38:10
2 18:38:11
3 18:38:12
4 18:38:13
…and so on…
```

-   Cannot stop it with Ctrl-C
-   Cannot background it with Ctrl-Z
-   Only way to stop it is `docker ps` to find ID and then `docker kill`
    -   Note: only have to give the first few digits of ID to `docker kill`

```{data-file="count_time_stop.text"}
$ docker ps
CONTAINER ID   IMAGE                 COMMAND                 CREATED         STATUS
741d896e4bb3   gvwilson/count-time   "/home/count_time.sh"   7 seconds ago   Up 6 seconds

$ docker kill 741d
```

## A Better Way

```{data-file="count_time_detach.text"}
$ docker container run --detach gvwilson/count-time
54c8c682a94a3853c62e2f86c19d463428a01452ed7e5cf85b076dcc0f447474

$ docker ps
CONTAINER ID   IMAGE                 COMMAND                 CREATED          STATUS
54c8c682a94a   gvwilson/count-time   "/home/count_time.sh"   12 seconds ago   Up 11 seconds

$ docker container stop 54c8
…wait a few seconds…

$
```

-   Use `--detach` to detach the container from the terminal that launched it
-   Use `docker container stop` to shut things down gracefully
-   Inspect output after the fact (or while the container is running) with `docker logs`

```{data-file="count_time_logs.text"}
$ docker logs 54c8
1 18:42:44
2 18:42:45
3 18:42:46
4 18:42:47
5 18:42:48
…more output…
```
