from flask import Flask, request, render_template, jsonify
import os
import subprocess
import sys
import json
import threading
from performai.config import NAMESPACES as DEFAULT_NAMESPACES, PROMETHEUS_URL as DEFAULT_PROMETHEUS_URL
from time import sleep  # For simulating delay (optional, for testing)

app = Flask(__name__)
analysis_results = {}
analysis_running = False

def run_performai_threaded(namespaces, prometheus_url):
    """Runs the performai main function in a separate thread."""
    global analysis_results
    global analysis_running
    analysis_running = True
    analysis_results['output'] = None
    analysis_results['error'] = False

    env = os.environ.copy()
    env['NAMESPACES'] = ",".join(namespaces)
    env['PROMETHEUS_URL'] = prometheus_url

    try:
        result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True, check=True, env=env)
        full_output = result.stdout.strip()

        # Try to find the start of the JSON output (assuming it starts with '[')
        json_start_index = full_output.find('[')
        if json_start_index != -1:
            json_output = full_output[json_start_index:]
            analysis_results['output'] = json_output
            analysis_results['error'] = False
        else:
            analysis_results['output'] = f"Error: Could not find JSON output in:\n{full_output}"
            analysis_results['error'] = True

    except subprocess.CalledProcessError as e:
        analysis_results['output'] = f"Error running performai: {e.stderr}"
        analysis_results['error'] = True
    except FileNotFoundError:
        analysis_results['output'] = "Error: main.py not found."
        analysis_results['error'] = True
    finally:
        analysis_running = False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        namespaces_str = request.form.get('namespaces')
        prometheus_url = request.form.get('prometheus_url')
        namespaces = [ns.strip() for ns in namespaces_str.split(',')] if namespaces_str else []

        global analysis_results
        analysis_results = {}  # Clear previous results
        global analysis_running
        analysis_running = True
        thread = threading.Thread(target=run_performai_threaded, args=(namespaces, prometheus_url))
        thread.start()
        return render_template('processing.html')

    return render_template('index.html', namespaces_input=", ".join(DEFAULT_NAMESPACES), prometheus_url_input=DEFAULT_PROMETHEUS_URL, analysis_running=analysis_running, results=analysis_results.get('output'), error=analysis_results.get('error', False))

@app.route('/status')
def status():
    return jsonify({'running': analysis_running, 'results': analysis_results.get('output'), 'error': analysis_results.get('error', False)})

@app.route('/results')
def results():
    results_output = analysis_results.get('output')
    error_status = analysis_results.get('error', False)
    recommendations = None
    error_message = None

    if error_status:
        error_message = results_output
    elif results_output:
        try:
            recommendations = json.loads(results_output)
        except json.JSONDecodeError:
            error_message = f"Error decoding JSON output: {results_output}"

    return render_template('results.html', recommendations=recommendations, error=error_message)

# @app.route('/results')
# def results():
#     print("Analysis Results in /results route:", analysis_results)
#     results_output = analysis_results.get('output')
#     error_status = analysis_results.get('error', False)
#     recommendations = None
#     error_message = None
#
#     if error_status:
#         error_message = results_output
#     elif results_output:
#         try:
#             recommendations = json.loads(results_output)
#         except json.JSONDecodeError:
#             error_message = f"Error decoding JSON output: {results_output}"
#
#     return render_template('results.html', recommendations=recommendations, error=error_message)

if __name__ == '__main__':
    app.run(debug=True)