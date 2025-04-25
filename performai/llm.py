import json
import requests
from performai.config import DEBUG

def call_local_llm(prompt: str) -> list:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    if response.status_code == 200:
        output = response.json().get("response", "")
        try:
            parsed = json.loads(output.strip())
            return [entry for entry in parsed if "recommend" in entry]
        except json.JSONDecodeError:
            print("⚠️ LLM response not valid JSON:", output)
            return []
    else:
        print(f"LLM error: {response.status_code} {response.text}")
        return []
