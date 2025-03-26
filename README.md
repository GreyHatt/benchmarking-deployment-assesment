# benchmarking-deployment-assesment 🚀

This project benchmarks **Cloud Run, Kubernetes (GKE), and Compute Engine (VM)** for a web workload.

## 📌 Tech Stack
- Python (Flask) for API
- Google Cloud Run (Serverless)
- Google Kubernetes Engine (GKE)
- Compute Engine (VM)
- GitHub Actions (CI/CD)

## 📌 Setup
1. Create a **GCP Service Account** and download the JSON key.
2. Set up GCP Secrets in GitHub.
3. Push code to **GitHub**, and it will **auto-deploy**!

## 📌 Run Locally
```sh
pip install -r app/requirements.txt
python app/app.py
```

## 📌 Repo Structure
📦 benchmarking_project
 ┣ 📂 app
 ┃ ┣ 📜 app.py                     # Flask API to trigger benchmarking and display results
 ┃ ┣ 📜 requirements.txt            # Dependencies for Flask and requests
 ┣ 📂 scripts
 ┃ ┣ 📜 benchmark_runner.py         # Unified script for benchmarking Serverless, Container, and VM
 ┣ 📂 infra
 ┃ ┣ 📜 Dockerfile                  # Dockerfile for containerized Flask API
 ┃ ┣ 📜 k8s-deployment.yaml         # Kubernetes Deployment YAML for GKE
 ┣ 📂 github-actions
 ┃ ┣ 📜 deploy.yml                  # GitHub Actions Workflow for CI/CD
 ┣ 📜 README.md                     # Documentation for the project
 ┣ 📜 .gitignore                    # Git ignore file
