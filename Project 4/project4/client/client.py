import json
import requests

endpoint = 'http://127.0.0.1:8000/api/posts/new/'

result = requests.post(endpoint, json={'content': 'all_working 2',})
print(result.json())