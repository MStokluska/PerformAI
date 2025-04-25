import subprocess
import json
import requests
from typing import List, Dict
from performai.config import PROMETHEUS_URL, LOOKBACK_DURATION, DEBUG
from performai.utils import cpu_to_millicores, bytes_to_mib

def get_k8s_workloads(namespace: str) -> List[Dict]:
    try:
        output = subprocess.check_output([
            "kubectl", "get", "deployments", "-n", namespace, "-o", "json"
        ])
        deployments = json.loads(output)
        result = []
        for dep in deployments["items"]:
            containers = dep['spec']['template']['spec']['containers']
            for container in containers:
                resources = container.get("resources", {})
                result.append({
                    "namespace": namespace,
                    "name": dep['metadata']['name'],
                    "container": container['name'],
                    "cpu_request": resources.get("requests", {}).get("cpu", "0"),
                    "cpu_limit": resources.get("limits", {}).get("cpu", "0"),
                    "mem_request": resources.get("requests", {}).get("memory", "0"),
                    "mem_limit": resources.get("limits", {}).get("memory", "0")
                })
        return result
    except Exception as e:
        print(f"Error fetching deployments for {namespace}: {e}")
        return []

def query_prometheus(query: str) -> float:
    response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": query})
    if response.status_code == 200:
        results = response.json()['data']['result']
        vals = [float(r['value'][1]) for r in results]
        return sum(vals) / len(vals) if vals else 0.0
    return 0.0

def get_usage_metrics(namespace: str, workload: str, container: str) -> Dict:
    if DEBUG:
        print(f"Checking workload: {workload}")
    cpu_query = f"avg_over_time(rate(container_cpu_usage_seconds_total{{namespace='{namespace}', pod=~'{workload}(-[a-z0-9]+)*', container='{container}'}}[5m])[{LOOKBACK_DURATION}:])"
    mem_query = f"avg_over_time(container_memory_usage_bytes{{namespace='{namespace}', pod=~'{workload}(-[a-z0-9]+)*', container='{container}'}}[{LOOKBACK_DURATION}])"
    cpu_avg = query_prometheus(cpu_query)
    mem_avg = query_prometheus(mem_query)
    if DEBUG:
        print(f"[DEBUG] Raw CPU avg for {workload}/{container}: {cpu_avg}")

    return {
        "cpu_avg": cpu_to_millicores(cpu_avg),
        "mem_avg": bytes_to_mib(mem_avg)
    }
