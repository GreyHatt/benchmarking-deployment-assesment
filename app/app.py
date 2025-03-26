from flask import Flask, jsonify, render_template
import time
import random
import requests
import subprocess
import threading
import os

app = Flask(__name__)

CLOUD_URL = os.environ(CLOUD_URL)
GKE_URL = os.environ(GKE_URL)
VM_URL = os.environ(VM_URL)


DEPLOYMENTS = {
    "Cloud Run": f"https://{CLOUD_URL}/benchmark",
    "GKE (Kubernetes)": f"https://{GKE_URL}/benchmark",
    "Compute Engine (VM)": f"http://{VM_URL}:8080/benchmark"
}

benchmark_results = {}

def benchmark_service(url, deployment_name):
    try:
        result = subprocess.run(['python3', 'scripts/benchmark_runner.py', url], capture_output=True, text=True)
        benchmark_results[deployment_name] = json.loads(result.stdout.strip())  # Parsing JSON output
    except Exception as e:
        benchmark_results[deployment_name] = {"error": f"Error: {e}"}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/benchmark')
def benchmark():
    threads = []
    for name, url in DEPLOYMENTS.items():
        thread = threading.Thread(target=benchmark_service, args=(url, name))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return jsonify(benchmark_results)

@app.route('/result')
def result():
    return jsonify(benchmark_results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

