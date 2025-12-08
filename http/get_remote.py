import requests

url = "https://gvwilson.github.io/sudonomicon/static/motto.txt"
response = requests.get(url)
print(f"status code: {response.status_code}")
print(f"body:\n{response.text}")
