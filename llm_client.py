import os
import time
import random
import requests
from dotenv import load_dotenv
load_dotenv()


# OPENROUTER CLIENT
class OpenRouterClient:

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found")

        self.model = "openrouter/owl-alpha"

        self.url = "https://openrouter.ai/api/v1/chat/completions"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "reporting-agent"
        }

    def generate(self, prompt: str, temperature: float = 0.3) -> str:

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 2500
        }

        for attempt in range(8):

            try:
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    json=payload,
                    timeout=120,
                )

                
                # RATE LIMIT HANDLING
                if response.status_code == 429:
                    wait = min(60, (2 ** attempt) + random.random())
                    print(f"[LLM] Rate limited → waiting {int(wait)}s")
                    time.sleep(wait)
                    continue

                if response.status_code != 200:
                    print("\n=== OPENROUTER ERROR ===")
                    print(response.text)
                    print("========================\n")
                    response.raise_for_status()
                data = response.json()

                msg = data.get("choices", [{}])[0].get("message", {})

                content = msg.get("content")

                
                # VALIDATION
                if isinstance(content, str) and content.strip():
                    return content.strip()
                print("[LLM WARNING] Empty response → retry")
                time.sleep(2)

            except Exception as e:
                print(f"[LLM WARNING] attempt {attempt + 1} failed:", str(e))
                time.sleep(2)

        raise RuntimeError("OpenRouter failed after retries")


class LLMRouter:

    def __init__(self):
        self.primary = OpenRouterClient()

    def generate(self, prompt: str, temperature: float = 0.3) -> str:
        print("[LLM ROUTER] Using Owl Alpha (single model)")
        return self.primary.generate(prompt, temperature)