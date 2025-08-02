import requests

url = "https://lessonomicon.github.io/sudonomicon/site/motto.json"
response = requests.get(url)
print(f"status code: {response.status_code}")
print(f"body as text: {len(response.text)} bytes")
as_json = response.json()
print(f"body as JSON:\n{as_json}")
