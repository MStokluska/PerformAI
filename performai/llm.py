import json
import requests
import os
from performai.config import DEBUG

USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "true").lower() == "true"
LLM_HOSTED_URL = os.getenv("LLM_HOSTED_URL")
LLM_API_TOKEN = os.getenv("LLM_API_TOKEN")
LLM_MODEL = os.getenv("LLM_MODEL", "mistral")  # default for local is "mistral"


def call_local_llm(prompt: str) -> list:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": LLM_MODEL,
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


def call_hosted_llm(prompt: str) -> list:
    """Call hosted LLM via HTTP endpoint (OpenAI-compatible format)."""
    headers = {
        "Authorization": f"Bearer {LLM_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a Kubernetes optimization assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(f"{LLM_HOSTED_URL}/v1/chat/completions", headers=headers, json=payload)
        
        if DEBUG:
            print(f"[DEBUG] Raw LLM response text: {response.text}")

        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']

            # Clean Markdown wrapping if present
            if content.startswith("```json"):
                content = content.strip().removeprefix("```json").removesuffix("```").strip()

            return json.loads(content)
        else:
            print(f"Hosted LLM error: {response.status_code} {response.text}")
            return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print("⚠️ Response that failed to parse:", response.text)
        return []
    except Exception as e:
        print(f"Hosted LLM exception: {e}")
        return []


def call_llm(prompt: str) -> list:
    if USE_LOCAL_LLM:
        return call_local_llm(prompt)
    else:
        return call_hosted_llm(prompt)
