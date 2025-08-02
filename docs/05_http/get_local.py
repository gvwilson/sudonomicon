import requests

URL = "http://localhost:8000/motto.txt"

response = requests.get(URL)
print(f"status code: {response.status_code}")
print(f"body:\n{response.text}")
