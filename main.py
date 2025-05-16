from performai.config import NAMESPACES, CHUNK_SIZE, DEBUG, LLM_HOSTED_URL, LLM_API_TOKEN, LLM_MODEL, PROMETHEUS_URL
from performai.collect import get_k8s_workloads, get_usage_metrics
from performai.utils import chunk_workloads
from performai.prompts import generate_prompt
from performai.llm import call_llm
import json
import os
import sys

def main():
    print("Main.py ran")
    # Store the original stdout
    original_stdout = sys.stdout

    # Redirect stdout to a temporary buffer (in memory)
    from io import StringIO
    sys.stdout = StringIO()

    namespaces_str = os.environ.get("NAMESPACES")
    if namespaces_str:
        namespaces = [ns.strip() for ns in namespaces_str.split(',')]
    else:
        namespaces = NAMESPACES  # Fallback to config if no env var

    prometheus_url = PROMETHEUS_URL
    if not prometheus_url:
        from performai.config import PROMETHEUS_URL as DEFAULT_PROMETHEUS_URL
        prometheus_url = DEFAULT_PROMETHEUS_URL

    all_workloads = []
    for ns in namespaces:
        workloads = get_k8s_workloads(ns)
        for w in workloads:
            usage = get_usage_metrics(w['namespace'], w['name'], w['container'])
            w.update(usage)
            all_workloads.append(w)

    recommendations = []
    for chunk in chunk_workloads(all_workloads, CHUNK_SIZE):
        prompt = generate_prompt(chunk)
        chunk_recs = call_llm(prompt)
        recommendations.extend(chunk_recs)

    #print(recommendations)
    print(json.dumps(recommendations, indent=2))

    # Get the JSON output from the buffer
    json_output = sys.stdout.getvalue()

    # Restore the original stdout
    sys.stdout = original_stdout

    # Print the JSON output to the actual stdout
    print(json_output)

    # Optional: Print debug info to stderr if DEBUG is True
    if DEBUG:
        print("Loaded Configuration (stderr):", file=sys.stderr)
        print(f"NAMESPACES: {NAMESPACES}", file=sys.stderr)
        print(f"PROMETHEUS_URL: {PROMETHEUS_URL}", file=sys.stderr)
        print(f"LLM_HOSTED_URL: {LLM_HOSTED_URL}", file=sys.stderr)
        print(f"LLM_API_TOKEN: {LLM_API_TOKEN}", file=sys.stderr)
        print(f"LLM_MODEL: {LLM_MODEL}", file=sys.stderr)
        print(f"LOOKBACK_DURATION: {os.environ.get('LOOKBACK_DURATION', '30d')}", file=sys.stderr)
        print(f"CHUNK_SIZE: {CHUNK_SIZE}", file=sys.stderr)
        print(f"DEBUG: {DEBUG}", file=sys.stderr)
        sys.stderr.flush()

if __name__ == "__main__":
     main()