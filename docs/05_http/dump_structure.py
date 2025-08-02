import requests
from requests_toolbelt.utils import dump

url = "https://lessonomicon.github.io/sudonomicon/site/motto.txt"
response = requests.get(url)
data = dump.dump_all(response)
print(str(data, "utf-8"))
