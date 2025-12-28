# Data Platform

## Overview

This project is all about building a **flexible, modular platform** for running **MLOps workloads** and backend services in Go, all on-premises. The idea is to provide a setup where infrastructure, data services, ML tools, pipelines, and APIs all work together in a **scalable and reproducible** way.

It should run in an Oracle Cloud as it has a better experience for free users. But just a kind reminder that I would choose Azure and get some services as ADLS, Azure SQL Databases, MongoDB and maybe Databricks/Fabric (optionally). Anyways, this architecture only requires K8S and it's cloud-agnostic.

### Main Components

- **Airflow** – Handles the orchestration of pipelines, including Spark jobs, MLflow experiments, Feast ingestion, and API tasks.  
  *Note:* The DAGs themselves are stored in a **separate repository**, so they can be versioned and deployed independently.  
- **Spark** – For batch and streaming data processing.  
- **MLflow** – Tracks experiments and stores registered models.  
- **Feast** – Manages features both offline and online.  
- **Seldon** – Deploys and serves ML models.  
- **FastAPI** – Hosts backend APIs.  
- **Kafka** – Manages messaging and streaming.  
- **Prometheus & Grafana** – Collect metrics, create dashboards, and handle alerts.  
- **Vault** – Keeps secrets safe and centralized.  
- **ArgoCD + Jenkins** – Handles CI/CD and GitOps workflows.  
- **Docker Registry** – Stores container images for all services.

---

## Folder Layout
```
data-platform/
├── infra/                # Core infrastructure and configuration
│   ├── terraform/        # Cluster, networking, and storage definitions
│   ├── vault/            # Secrets and policies
│   ├── prometheus/       # Monitoring configs and alert rules
│   ├── grafana/          # Dashboards and datasources
│   └── docker-registry/  # Container registry configs
│
├── apps/                 # Microservices and platform apps
│   ├── airflow/          # Airflow deployment (DAGs repo separate)
│   ├── spark/            # Spark jobs, configs, Dockerfile
│   ├── mlflow/           # MLflow service configs
│   ├── feast/            # Feature store configs
│   ├── seldon/           # Model serving configs
│   ├── fastapi/          # Backend APIs
│   └── kafka/            # Kafka brokers, connectors, configs
│
├── argocd/               # GitOps setup: ArgoCD projects and apps
│   ├── projects/         # ArgoCD project definitions
│   └── apps/             # YAMLs pointing to app manifests
│       ├── airflow.yaml
│       ├── spark.yaml
│       ├── mlflow.yaml
│       ├── feast.yaml
│       ├── seldon.yaml
│       ├── fastapi.yaml
│       └── kafka.yaml
│
├── docs/ # Documentation
└── scripts/ # Helper scripts for initializing infra, CI/CD, etc.
```

---

## Airflow DAGs

The Airflow DAGs live in a **separate repository**. This makes it easy to:

- Version and track pipelines independently.  
- Run CI/CD pipelines separately from the platform infra.  
- Treat pipelines like microservices that can evolve on their own.

In this repo, Airflow is **just the runtime environment**, connecting to the DAGs repo through GitSync or a mounted volume. The DAGs orchestrate tasks across services like Spark, MLflow, Feast, Seldon, and FastAPI.

---

## Observability

- Metrics for infrastructure and pipelines are collected with **Prometheus**.  
- Dashboards and alerts are available in **Grafana**.  
- Logs can be centralized using **Loki** or any other logging backend.

---

## Secrets and Configuration

- **Vault** manages all secrets.  
- **Important:** Never commit secrets to Git.

---

## Workflow

1. **ArgoCD** keeps the cluster in sync with manifests from this repo.  
2. **Jenkins** builds images, runs tests, and updates container versions.  
3. **Airflow** runs DAGs from the separate DAGs repository.  
4. DAGs then orchestrate:
   - **Spark jobs** from `apps/spark/`  
   - **MLflow experiments and model registrations** from `apps/mlflow/`  
   - **Feature store ingestion** from `apps/feast/`  
   - **Model serving deployments/checks** from `apps/seldon/`  
   - **API tasks** from `apps/fastapi/`  
5. Data itself is stored in **MinIO**, and DAGs reference it via logical paths (`raw → staging → curated`).

---

## Contributing

1. Create a branch from `main`.  
2. Make changes in the appropriate folder (`apps/*` or `infra/*`).  
3. Submit a pull request for review.  
4. CI/CD through Jenkins/ArgoCD handles safe deployment.
