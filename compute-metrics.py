import requests,time,subprocess
import pandas as pd
from google.cloud import billing

DEPLOYMENTS = {
    "Serverless": "https://YOUR_CLOUD_RUN_URL/process",
    "Container": "https://YOUR_GKE_URL/process",
    "VM": "http://YOUR_VM_IP:8080/process"
}

# For Response time
def test_response_time(url, num_requests=100):
    times = []
    for _ in range(num_requests):
        start_time = time.time()
        response = requests.post(url, json={"input": "test_data"})
        end_time = time.time()
        
        if response.status_code == 200:
            times.append(end_time - start_time)
        else:
            print(f"Error: {response.status_code} - {response.text}")
    
    return round(sum(times) / len(times), 4) if times else None

# For Deployement times
def measure_deployment_time(deployment):
    if deployment == "Serverless":
        command = ["gcloud", "run", "deploy", "YOUR_SERVICE_NAME", "--format=json"]
    elif deployment == "Container":
        command = ["gcloud", "container", "clusters", "describe", "YOUR_CLUSTER_NAME", "--format=json"]
    elif deployment == "VM":
        command = ["gcloud", "compute", "instances", "describe", "YOUR_INSTANCE_NAME", "--format=json"]
    else:
        return None
    
    try:
        start_time = time.time()
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end_time = time.time()
        return round(end_time - start_time, 2)
    except Exception as e:
        print(f"Error measuring deployment time for {deployment}: {e}")
        return None

# To get Costings
def get_gcp_cost(deployment):
    billing_client = billing.CloudBillingClient()
    billing_account = "billingAccounts/YOUR_BILLING_ACCOUNT_ID"
    
    service_map = {
        "Serverless": "services/6F81-5844-456A",
        "Container": "services/F508-5C1E-51FD",
        "VM": "services/DA34-426B-42BA"
    }
    
    service_id = service_map.get(deployment)
    if not service_id:
        return None
    
    try:
        request = billing.ListSkusRequest(parent=service_id)
        skus = billing_client.list_skus(request=request)
        
        for sku in skus:
            if "cost" in str(sku):
                return round(sku.pricing_info[0].pricing_expression.tiered_rates[0].unit_price.nanos / 1e9, 4)
        
    except Exception as e:
        print(f"Error fetching cost for {deployment}: {e}")
        return None

# Execute Benchmarking
num_requests = 100
results = []

for deployment, url in DEPLOYMENTS.items():
    print(f"Testing: {deployment} ...")
    
    avg_response_time = test_response_time(url, num_requests)
    deployment_time = measure_deployment_time(deployment)
    estimated_cost = get_gcp_cost(deployment)

    results.append({
        "Deployment": deployment,
        "Avg Response Time (s)": avg_response_time,
        "Deployment Time (s)": deployment_time,
        "Estimated Cost ($/request)": estimated_cost
    })

df = pd.DataFrame(results)
df.to_csv("benchmark_results.csv", index=False)

print(" ... Benchmarking Completed! Results saved to 'benchmark_results.csv' ... ")
