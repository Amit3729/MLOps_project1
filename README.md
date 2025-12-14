# 🚀 End-to-End MLOps Project

> **Production‑grade Machine Learning System with MongoDB, AWS, Docker, CI/CD, and Model Deployment**

This project demonstrates a **complete MLOps lifecycle**, from raw data ingestion to automated deployment on AWS. It is designed to **impress recruiters and technical reviewers** by showcasing real‑world tools, best practices, and scalable architecture used in modern ML engineering.

---

## 📌 Key Highlights

* Modular & scalable **project template**
* **MongoDB Atlas** for cloud data storage
* Robust **logging & exception handling**
* End‑to‑end **ML pipeline** (Ingestion → Validation → Transformation → Training → Evaluation → Pushing)
* **AWS S3** for model registry
* **Dockerized application**
* **CI/CD pipeline** using GitHub Actions
* **Deployment on AWS EC2** using a self‑hosted runner
* Production‑ready **prediction pipeline with Flask**

---

## 🏗️ Project Structure Overview

```
├── artifact/                # Generated artifacts (ignored in git)
├── config/                  # Schema & configuration files
├── notebook/                # EDA & MongoDB demo notebooks
├── src/
│   ├── components/          # ML pipeline components
│   ├── configuration/       # MongoDB & AWS connections
│   ├── constants/           # Project-wide constants
│   ├── data_access/         # Data fetching logic
│   ├── entity/              # Config & artifact entities
│   ├── aws_storage/         # S3 push/pull logic
│   ├── utils/               # Common utilities
│   └── pipeline/            # Training & prediction pipelines
├── static/                  # Frontend static files
├── templates/               # HTML templates
├── app.py                   # Flask application
├── Dockerfile
├── requirements.txt
├── setup.py
├── pyproject.toml
└── .github/workflows/aws.yaml
```

---

## ⚙️ Project Setup & Initialization

### 1️⃣ Project Template Creation

```bash
python template.py
```

This initializes a clean, modular MLOps project structure.

---

### 2️⃣ Local Package Management

* Implemented `setup.py` and `pyproject.toml`
* Enables importing the project as a **local Python package**
* Follows industry‑standard packaging practices

📄 Detailed explanations available in `course.txt`

---

### 3️⃣ Virtual Environment Setup

```bash
conda create -n env_name python=3.12
conda activate env_name
pip install -r requirements.txt
```

Verify installed packages:

```bash
pip list
```

---

## 🍃 MongoDB Atlas Integration

### 4️⃣ MongoDB Cloud Setup

* Created MongoDB Atlas account & project
* Deployed a cluster
* Configured DB user & public network access
* Generated Python connection string (Python 3.12)

---

### 5️⃣ Data Upload via Notebook

* Created `notebook/mongodb_demo.ipynb`
* Loaded dataset
* Inserted data into MongoDB Atlas
* Verified data in **Key‑Value (Document) format** via Atlas UI

---

## 🧾 Logging, Exception Handling & EDA

* Custom `logger.py` implemented and tested via `demo.py`
* Centralized `exception.py` for robust error handling
* Added EDA & Feature Engineering notebooks

✔ Improves debuggability and production stability

---

## 🔄 Data Ingestion Pipeline

### 6️⃣ Configuration & Constants

* Defined variables in `constants/__init__.py`
* MongoDB connection logic in `mongo_db_connection.py`

### 7️⃣ Data Access Layer

* `proj1_data.py` fetches data from MongoDB
* Converts key‑value documents into Pandas DataFrame

### 8️⃣ Entity & Component Design

* `DataIngestionConfig`
* `DataIngestionArtifact`
* `data_ingestion.py`

### 9️⃣ Environment Variable Setup

```bash
export MONGODB_URL="your_connection_string"
echo $MONGODB_URL
```

🚫 `artifact/` directory added to `.gitignore`

---

## ✅ Data Validation, Transformation & Training

### 🔍 Data Validation

* Dataset schema defined in `config/schema.yaml`
* Validation logic implemented using `utils/main_utils.py`

### 🔄 Data Transformation

* Feature engineering & preprocessing
* Estimator logic added in `entity/estimator.py`

### 🤖 Model Training

* Training pipeline implemented
* Trained models stored as artifacts

---

## ☁️ AWS Setup (Model Registry & Deployment)

### 1️⃣ IAM & Credentials

* IAM user with `AdministratorAccess`
* Access keys configured as environment variables

```bash
export AWS_ACCESS_KEY_ID='xxxx'
export AWS_SECRET_ACCESS_KEY='xxxx'
```

---

### 2️⃣ S3 Model Registry

* Created S3 bucket (region: `us-east-1`)
* Configured constants:

```python
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE = 0.02
MODEL_BUCKET_NAME = "your-bucket-name"
MODEL_PUSHER_S3_KEY = "model-registry"
```

* Implemented S3 push/pull logic
* `s3_estimator.py` handles model versioning

---

## 📊 Model Evaluation & Model Pusher

* Compares new model vs production model
* Pushes best model to AWS S3 automatically

---

## 🔮 Prediction Pipeline & Web App

* Flask‑based prediction pipeline
* `app.py` exposes training & prediction routes
* Integrated frontend using `static/` & `templates/`

---

## 🐳 Docker & CI/CD Pipeline

### Dockerization

* Dockerfile & `.dockerignore` added
* Image built for production deployment

---

### GitHub Actions CI/CD

* Workflow defined in `.github/workflows/aws.yaml`
* Secrets configured:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
ECR_REPO
```

---

## 🚢 AWS ECR & EC2 Deployment

### ECR

* Created ECR repository
* Docker images pushed automatically

### EC2

* Ubuntu server launched
* Docker installed
* GitHub self‑hosted runner configured

```bash
./config.sh
./run.sh
```

---

## 🌐 Application Access

* Opened port **5001** in EC2 Security Group

```
http://<EC2_PUBLIC_IP>:5001
```

✔ Application is live and ready for training & prediction

---

## 🎯 What This Project Demonstrates

✅ Real‑world MLOps architecture
✅ Cloud‑native ML pipelines
✅ Production deployment on AWS
✅ CI/CD automation
✅ Scalable & maintainable codebase

---

## 👨‍💻 Author

**Amit Pal**
Aspiring Data Scientist | ML Engineer | MLOps Enthusiast

---

⭐ *If you're a recruiter or reviewer: this project reflects industry‑ready MLOps skills and deployment experience.*
