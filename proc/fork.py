import os

print(f"starting {os.getpid()}")
pid = os.fork()
if pid == 0:
    print(f"child got {pid} is {os.getpid()}")
else:
    print(f"parent got {pid} is {os.getpid()}")
