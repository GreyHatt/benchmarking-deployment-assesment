# benchmarking-deployment-assesment
📦 benchmarking_project
 ┣ 📂 app
 ┃ ┣ 📜 app.py                     # Flask API for benchmarking
 ┃ ┣ 📜 requirements.txt            # Dependencies
 ┣ 📂 scripts
 ┃ ┣ 📜 benchmark_runner.py         # Main script to benchmark different deployments
 ┃ ┣ 📜 gcp_billing_api.py          # Script to estimate cost using GCP Billing API
 ┣ 📂 infra
 ┃ ┣ 📜 Dockerfile                  # Docker setup for container-based deployment
 ┃ ┣ 📜 deployment.yaml              # Kubernetes deployment YAML
 ┣ 📂 github-actions
 ┃ ┣ 📜 deploy.yml                   # GitHub Actions Workflow for GCP Deployment
 ┣ 📜 README.md                      # Project Documentation
 ┣ 📜 .gitignore                      # Ignore unnecessary files