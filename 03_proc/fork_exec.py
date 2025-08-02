import os
import sys

print(f"starting {os.getpid()}")
sys.stdout.flush()
pid = os.fork()
if pid == 0:
    os.execl("/bin/echo", "echo", f"child echoing {pid} from {os.getpid()}")
else:
    print(f"parent got {pid} is {os.getpid()}")
