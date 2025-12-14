End-to-End MLOps Project
A Production-Ready Machine Learning Pipeline with Cloud Integration and CI/CD
This project demonstrates a complete MLOps implementation, from data ingestion to model deployment. It showcases best practices in modular code structure, cloud storage, containerization, and automated CI/CD pipelines.
ml-ops.orgtowardsdatascience.commedium.com


Key Technologies & Tools









































CategoryTechnologies/ServicesLanguage & FrameworkPython, Flask (for prediction API)DatabaseMongoDB Atlas (Cloud NoSQL)Cloud StorageAWS S3 (Model Registry)ContainerizationDockerCI/CDGitHub Actions (Self-hosted runner on AWS EC2)InfrastructureAWS EC2 (Deployment), AWS ECR (Docker Registry), AWS IAMPipeline ComponentsCustom modular components: Data Ingestion, Validation, Transformation, Training, Evaluation, PusherOthersLogging, Custom Exceptions, EDA Notebooks, Virtual Environments
mongodb.comaws.plainenglish.iodocker.comblog.devgenius.iolevelup.gitconnected.com




Project Features

Modular Architecture: Clean separation of concerns using components/, entity/, configuration/, and pipeline/ directories.
Data Handling: Ingestion from MongoDB Atlas, validation against schema, transformation, and feature engineering.
Model Management: Training, evaluation with threshold-based change detection, and pushing to AWS S3 registry.
Production Readiness: Flask-based prediction API, Docker containerization.
Automated Deployment: Full CI/CD pipeline using GitHub Actions, self-hosted on EC2, with ECR for images.
Best Practices: Custom logging, exception handling, virtual environments, .gitignore for artifacts.

Project Structure Overview
textproject/
├── src/
│   ├── components/     # Data Ingestion, Validation, Transformation, Trainer, Evaluation, Pusher
│   ├── configuration/  # MongoDB & AWS connections
│   ├── entity/         # Config & Artifact entities, estimators
│   ├── pipeline/       # Training & Prediction pipelines
│   ├── utils/          # Main utilities
│   └── aws_storage/    # S3 operations
├── notebook/           # EDA, Feature Engineering, MongoDB demo
├── app.py              # Flask prediction app
├── template/ & static/ # Web UI assets
├── Dockerfile
├── requirements.txt
├── setup.py / pyproject.toml
└── .github/workflows/  # CI/CD yaml
Quick Setup & Run Guide
1. Project Initialization
Bashpython template.py  # Create project structure
# Configure setup.py and pyproject.toml for local package import
2. Environment Setup
Bashconda create -n mlops_env python=3.12
conda activate mlops_env
pip install -r requirements.txt
3. MongoDB Atlas Setup

Create cluster, database user, allow network access.
Get Python connection string and set environment variable:

Bashexport MONGODB_URL="mongodb+srv://<user>:<pass>@cluster..."
4. Data Ingestion & Pipeline

Update constants/__init__.py, configuration files.
Run demo.py to test ingestion.
Execute training pipeline for full flow.

5. AWS Setup for Model Registry

Create IAM user with AdministratorAccess.
Create S3 bucket.
Set environment variables:

Bashexport AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
6. Deployment & CI/CD

Build Docker image.
Setup ECR repository.
Configure self-hosted GitHub Actions runner on EC2.
Add secrets in GitHub repo.
On push, pipeline builds, pushes to ECR, deploys to EC2.
Access app at http://<EC2_PUBLIC_IP>:5001

This project highlights expertise in building scalable, production-grade ML systems with modern DevOps practices. Perfect for demonstrating MLOps proficiency! 🚀1.6s
