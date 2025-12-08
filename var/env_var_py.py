# env_var_py.py
import os

window = os.getenv("WINDOW", default="not set")
threshold = os.getenv("THRESHOLD", default="not set")
print(f"inner: window is {window} and threshold is {threshold}")
