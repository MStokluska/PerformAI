import json

def generate_prompt(workload_summary):
    prompt = """
You are an expert Kubernetes resource optimizer.

Given a list of workloads, compare their actual CPU and memory usage with their configured requests and limits. Recommend adjustments **only** when they are significantly different (more than 30%) from the average usage.

Follow these rules:
- Always round CPU requests/limits to the nearest 50m
- Always round memory requests/limits to the nearest 64Mi
- Never set CPU request below 100m
- Never set memory request below 128Mi
- Limit values should not be lower than their respective requests

Respond only with JSON in the following format:

[
  {
    "namespace": "...",
    "name": "...",
    "container": "...",
    "recommend": {
      "cpu_request": "...",
      "cpu_limit": "...",
      "mem_request": "...",
      "mem_limit": "..."
    }
  }
]

Example:
[
  {
    "namespace": "example",
    "name": "webapp",
    "container": "main",
    "cpu_request": "250m",
    "cpu_limit": "500m",
    "mem_request": "192Mi",
    "mem_limit": "256Mi"
  }
]

Workloads:
""" + json.dumps(workload_summary, indent=2) + "\n\nReturn only valid JSON."
    return prompt

