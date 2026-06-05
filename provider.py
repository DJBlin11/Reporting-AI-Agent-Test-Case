import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_model_endpoints():
    url = "https://openrouter.ai/api/v1/models/openrouter/owl-alpha/endpoints"
    headers = {"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("Доступные эндпоинты:")
        for endpoint in data.get("data", {}).get("endpoints", []):
            print(f"  - Провайдер: {endpoint.get('provider_name')}")
            print(f"    Статус: {endpoint.get('status')}")
            print(f"    Задержка: {endpoint.get('latency_ms')}ms")
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)

get_model_endpoints()