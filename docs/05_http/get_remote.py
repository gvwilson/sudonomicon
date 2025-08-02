import requests

url = "https://lessonomicon.github.io/sudonomicon/site/motto.txt"
response = requests.get(url)
print(f"status code: {response.status_code}")
print(f"body:\n{response.text}")
