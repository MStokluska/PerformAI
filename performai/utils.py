def bytes_to_mib(val: float) -> str:
    mib = val / (1024 ** 2)
    rounded = max(128, round(mib / 64) * 64)
    return f"{rounded}Mi"

def cpu_to_millicores(val: float) -> str:
    return f"{max(round(val * 1000), 50)}m"

def chunk_workloads(workloads, size):
    return [workloads[i:i + size] for i in range(0, len(workloads), size)]
