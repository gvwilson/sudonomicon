import requests
import sys

URL = sys.argv[1]

response = requests.get(URL)
print(f"status code: {response.status_code}")
print(f"body:\n{response.text}")
