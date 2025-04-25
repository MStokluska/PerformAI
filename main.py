from performai.config import NAMESPACES, CHUNK_SIZE
from performai.collect import get_k8s_workloads, get_usage_metrics
from performai.utils import chunk_workloads
from performai.prompts import generate_prompt
from performai.llm import call_llm
import json


def main():
    all_workloads = []
    for ns in NAMESPACES:
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

    print("\nRecommendations:")
    print(json.dumps(recommendations, indent=2))


if __name__ == "__main__":
    main()
