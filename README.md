# PerformAI [WIP]

**PerformAI** is a modular Python tool that connects to a Kubernetes cluster, analyzes CPU and memory usage of workloads using Prometheus metrics, and generates optimization recommendations using a local LLM (like Mistral 7B via Ollama).

---

## 🚀 Features
- Targets only specific namespaces
- Pulls resource usage from Prometheus over configured lookback duration
- Compares with actual CPU/Memory requests & limits
- Uses local LLM (Mistral 7B) to recommend adjustments

---

## 📦 Requirements
- Python 3.9+
- Prometheus endpoint accessible
- `kubectl` configured and authenticated
- [Ollama](https://ollama.com/) running locally with the `mistral` model:
  ```bash
  ollama run mistral
  ```

---

## 🔧 Setup
```bash
git clone https://github.com/yourusername/performAI.git
cd performAI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🛠 Configuration
Edit `performai/config.py` to set:
- Target namespaces
- Prometheus endpoint
- Lookback window for metrics

---

## 🧠 Usage
```bash
python main.py
```
---

## 📂 Project Structure
```
performai/
├── config.py
├── collect.py
├── prompts.py
├── llm.py
├── utils.py          
main.py
```

---

## 📜 License
MIT
