import requests

payload = {
  "message": "Hello, my name is John Doe. I am a new user",
}
headers = {}
url = "http://127.0.0.1:8000/chai_api/"

response = requests.post(url, json=payload, headers=headers)

print(response.json())
