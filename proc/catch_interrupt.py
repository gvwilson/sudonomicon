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
