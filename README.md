🚀 MLOps Project: End-to-End Machine Learning Pipeline

Welcome to my MLOps Project, an end-to-end machine learning workflow demonstrating data ingestion, processing, model training, evaluation, deployment, and CI/CD automation. This project showcases my expertise in Python, MongoDB, AWS, Docker, and CI/CD pipelines, and provides a robust template for scalable machine learning applications.

🌟 Project Overview

This project implements a full MLOps pipeline, including:

Project scaffolding & modular Python package setup

Data ingestion from MongoDB

Logging and exception handling

Data validation, transformation, and feature engineering

Model training, evaluation, and deployment

CI/CD automation using GitHub Actions, Docker, AWS ECR, and EC2

AWS S3 integration for model storage and versioning

Web app interface for prediction and monitoring

🛠 Technologies & Tools Used
Layer	Tools & Libraries
Programming	Python 3.12, Jupyter Notebooks
Data Storage	MongoDB Atlas
Data Processing	pandas, numpy
Logging & Exception Handling	Python logging, custom exception modules
Machine Learning	scikit-learn, custom pipelines
AWS Services	S3 (model storage), IAM (access control), EC2 (deployment), ECR (container registry)
Containerization & CI/CD	Docker, GitHub Actions, Self-hosted runner on EC2
Web Interface	 HTML templates
⚡ Project Setup
1. Project Scaffolding
# Create project template
python template.py

# Setup local package
# Add code in setup.py and pyproject.toml

2. Environment Setup
# Create virtual environment
conda create -n env_name python=3.12
conda activate env_name

# Install required dependencies
pip install -r requirements.txt

# Check installed packages
pip list

🗄 MongoDB Setup

Signup to MongoDB Atlas and create a new project & cluster

Create DB user and configure network access (allow public access)

Get connection string for Python driver (Python 3.12)

Create notebook/mongodb_demo.ipynb for testing

Add datasets and push data to MongoDB

Verify data in MongoDB Atlas (key-value format)

📓 Logging, Exception Handling & EDA

Custom logger and exception modules created and tested

EDA and feature engineering notebooks prepared for dataset insights

🏗 Data Ingestion Pipeline

Define constants in constants/__init__.py

Configure MongoDB connection in mongo_db_connection.py

Fetch data in proj1_data.py and transform into pandas DataFrame

Define DataIngestionConfig and DataIngestionArtifact classes

Implement data_ingestion.py and integrate with training pipeline

Run demo.py with MongoDB URL set:

# PowerShell
$env:MONGODB_URL="your_connection_string"

# Bash
export MONGODB_URL="your_connection_string"


Note: Add artifact folder to .gitignore

🔄 Data Validation, Transformation & Model Training

Define dataset schema in config/schema.yaml

Implement utility functions in utils/main_utils.py

Develop Data Validation, Data Transformation, and Model Trainer components

Use estimator.py for ML estimator configurations

☁ AWS Integration

IAM Setup: Create user with Admin access and configure access keys

Environment Variables:

export AWS_ACCESS_KEY_ID='YOUR_ACCESS_KEY_ID'
export AWS_SECRET_ACCESS_KEY='YOUR_SECRET_ACCESS_KEY'
export AWS_DEFAULT_REGION='us-east-1'


S3 Bucket Setup: Model storage and retrieval via src/aws_storage and s3_estimator.py

Constants for model evaluation:

MODEL_EVULATION_CHANGED_THRESHOLD_SCORE = 0.02
MODEL_BUCKET_NAME = "my-model-proj7"
MODEL_PUSHER_S3_KEY = "model-registry"

🚀 Model Deployment & Prediction

Create prediction pipeline and setup app.py

Add static and template directories for web interface

Expose EC2 port 5001 for app access

Access web app: http://<EC2_PUBLIC_IP>:5001

🛠 CI/CD Pipeline

Dockerize project using Dockerfile and .dockerignore

Configure GitHub Actions in .github/workflows/aws.yaml

Connect GitHub to self-hosted EC2 runner

Push Docker images to AWS ECR

CI/CD pipeline triggers on code commits

EC2 instance runs Dockerized ML app

📂 Directory Structure (Key Files)
├── src/
│   ├── configuration/
│   │   └── mongo_db_connection.py
│   │   └── aws_connection.py
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluation.py
│   │   └── model_pusher.py
│   ├── aws_storage/
│   │   └── s3_estimator.py
│   └── entity/
│       ├── config_entity.py
│       ├── artifact_entity.py
│       └── estimator.py
├── notebook/
│   └── mongodb_demo.ipynb
├── requirements.txt
├── setup.py
├── pyproject.toml
├── Dockerfile
└── app.py

🌟 Highlights

Full MLOps workflow from data ingestion to deployment

Integration with MongoDB, AWS S3, and EC2

Custom logging, exception handling, and pipeline classes

CI/CD automation using GitHub Actions and Docker

Web interface for real-time predictions
