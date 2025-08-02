import requests

url = "https://lessonomicon.github.io/sudonomicon/site/nonexistent.txt"
response = requests.get(url)
print(f"status code: {response.status_code}")
print(f"body length: {len(response.text)}")
