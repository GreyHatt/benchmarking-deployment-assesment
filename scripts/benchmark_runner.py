import requests
import sys
import time

def benchmark_service(url):
    start_time = time.time()
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        response_time = time.time() - start_time
        return response_time
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python benchmark_runner.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    response_time = benchmark_service(url)
    print(f"Response time for {url}: {response_time} seconds")
