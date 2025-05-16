import sys

import requests
import json
from performai.config import USE_LOCAL_LLM, LLM_HOSTED_URL, LLM_API_TOKEN, LLM_MODEL, DEBUG

def call_local_llm(prompt: str, llm_model: str = "mistral") -> list:  # add defaults
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": llm_model,
            "prompt": prompt,
            "stream": False
        }
    )
    if response.status_code == 200:
        output = response.json().get("response", "")
        if DEBUG:
            print(f"[DEBUG] Local LLM Response: {output}", file=sys.stderr)
        try:
            parsed = json.loads(output.strip())
            return [entry for entry in parsed if "recommend" in entry]
        except json.JSONDecodeError:
            print("⚠️ LLM response not valid JSON:", output, file=sys.stderr)
            return []
    else:
        print(f"LLM error: {response.status_code} {response.text}", file=sys.stderr)
        return []


def call_hosted_llm(prompt: str, llm_hosted_url: str, llm_api_token: str, llm_model: str) -> list:
    """Call hosted LLM via HTTP endpoint (OpenAI-compatible format)."""
    headers = {
        "Authorization": f"Bearer {llm_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "model": llm_model,
        "messages": [
            {"role": "system", "content": "You are a Kubernetes optimization assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(f"{llm_hosted_url}/v1/chat/completions", headers=headers, json=payload)

        if DEBUG:
            print(f"[DEBUG] Raw LLM response text: {response.text}", file=sys.stderr)

        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']

            # Clean Markdown wrapping if present
            if content.startswith("```json"):
                content = content.strip().removeprefix("```json").removesuffix("```").strip()
            if DEBUG:
                print(f"[DEBUG] Processed LLM response text: {content}", file=sys.stderr)
            return json.loads(content)
        else:
            print(f"Hosted LLM error: {response.status_code} {response.text}", file=sys.stderr)
            return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}  Response that failed to parse: {response.text}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Hosted LLM exception: {e}", file=sys.stderr)
        return []


def call_llm(prompt: str, llm_hosted_url: str = "", llm_api_token: str = "", llm_model: str = "mistral") -> list:
    if USE_LOCAL_LLM:
        print("do I get here ?")
        return call_local_llm(prompt, llm_model)
    else:
        if llm_hosted_url == "":
            llm_hosted_url = LLM_HOSTED_URL
            llm_api_token = LLM_API_TOKEN
            llm_model = LLM_MODEL

        return call_hosted_llm(prompt, llm_hosted_url, llm_api_token, llm_model)
