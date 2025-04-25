from flask import Flask, request, render_template, jsonify
import os
import subprocess
import sys
import json
from performai.config import NAMESPACES as DEFAULT_NAMESPACES, PROMETHEUS_URL as DEFAULT_PROMETHEUS_URL

app = Flask(__name__)

def run_performai(namespaces, prometheus_url):
    """Runs the performai main function with provided NAMESPACES and PROMETHEUS_URL."""
    env = os.environ.copy()
    env['NAMESPACES'] = ",".join(namespaces)
    env['PROMETHEUS_URL'] = prometheus_url

    try:
        result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True, check=True, env=env)
        return result.stdout, False  # Return stdout and False for no error
    except subprocess.CalledProcessError as e:
        return f"Error running performai: {e.stderr}", True
    except FileNotFoundError:
        return "Error: main.py not found.", True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        namespaces_str = request.form.get('namespaces')
        prometheus_url = request.form.get('prometheus_url')
        namespaces = [ns.strip() for ns in namespaces_str.split(',')] if namespaces_str else []

        output, error = run_performai(namespaces, prometheus_url)
        if error:
            return render_template('index.html', error=output, namespaces_input=namespaces_str, prometheus_url_input=prometheus_url)
        try:
            recommendations = json.loads(output.strip())
            return render_template('results.html', recommendations=recommendations)
        except json.JSONDecodeError:
            return render_template('index.html', error=f"Error decoding JSON output: {output}", namespaces_input=namespaces_str, prometheus_url_input=prometheus_url)

    return render_template('index.html', namespaces_input=", ".join(DEFAULT_NAMESPACES), prometheus_url_input=DEFAULT_PROMETHEUS_URL)

if __name__ == '__main__':
    app.run(debug=True)