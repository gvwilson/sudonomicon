import requests

url = "https://gvwilson.github.io/sudonomicon/site/motto.txt"
response = requests.get(url)
for key, value in response.headers.items():
    print(f"{key}: {value}")
