# [create]
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
# [/create]

# [lockdown]
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
# [/lockdown]

# [enable]
os.chmod(filename, stat.S_IRUSR + stat.S_IWUSR)
status = os.stat(filename)
print(stat.filemode(status.st_mode))
# -rw-------
# [/enable]
