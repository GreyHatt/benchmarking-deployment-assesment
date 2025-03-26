import requests
import time
import sys
import threading
from googleapiclient.discovery import build
from google.auth import exceptions
import os

# Function to make HTTP requests and return response time
def benchmark_service(url, request_count=100):
    start_time = time.time()
    successful_requests = 0

    # Simulate load (multiple concurrent requests)
    def send_request():
        nonlocal successful_requests
        try:
            response = requests.get(url)
            if response.status_code == 200:
                successful_requests += 1
        except requests.exceptions.RequestException as e:
            pass  # Ignore errors
    
    # Running concurrent requests
    threads = []
    for _ in range(request_count):
        thread = threading.Thread(target=send_request)
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    completion_time = time.time() - start_time
    avg_response_time = completion_time / request_count if successful_requests else 0

    return {
        "total_time": completion_time,
        "avg_response_time": avg_response_time,
        "successful_requests": successful_requests,
        "concurrent_requests": request_count
    }

# Function to get the estimated cost using GCP Billing API
def get_gcp_cost(project_id):
    try:
        service = build('cloudbilling', 'v1')
        billing_info = service.projects().getBillingInfo(name=f'projects/{project_id}').execute()

        if billing_info.get('billingEnabled'):
            return {"cost_estimate": "Estimate available after billing usage."}
        else:
            return {"error": "Billing not enabled for this project."}
    except exceptions.GoogleAuthError as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python benchmark_runner.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    request_count = 100
    project_id = os.environ("GCP_PROJECT_ID")

    # Benchmark the service
    benchmark_result = benchmark_service(url, request_count)
    
    # Get GCP cost
    cost = get_gcp_cost(project_id)

    result = {
        "benchmark_result": benchmark_result,
        "cost": cost
    }

    # Output results as JSON
    print(str(result))

