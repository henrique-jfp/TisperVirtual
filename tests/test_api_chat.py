import json
import requests
url = "http://127.0.0.1:8000/api/chat"
payload = {"prompt": "Teste de integração: olá mundo", "chat_history": []}
data = json.dumps(payload).encode('utf-8')
try:
    response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
except Exception as e:
    print(f"An error occurred while making the API request: {e}")
else:
    if response.status_code == 200:
        result = response.json()
        print(result)
    else:
        print(f"API request failed with status code: {response.status_code}")

