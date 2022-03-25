import json
import requests

endpoint = 'http://127.0.0.1:8000/api/posts/new/'

result = requests.get(endpoint, json={'message': 'all_working'})
print(result.json())