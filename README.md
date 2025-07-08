# 🛡️ Threat Intelligence Dashboard

A full-stack dashboard for ingesting, analyzing, and visualizing cybersecurity threat intelligence data. Built using Flask, MongoDB, React, and Docker to ensure fast performance, scalable architecture, and ease of deployment.

---

## 📌 Features

- 🔍 Ingests structured CSV threat data into MongoDB
- 📊 Visualizes real-time stats by threat category and severity
- 📂 Browse and filter threat records
- 📦 Fully containerized with Docker and Docker Compose
- 🧠 Analyze threat descriptions using ML to auto-classify them

---

## 💡 Why This Stack?

| Component          | Technology           |Justification                                                                
|--------------------|----------------------|------------------------------------------------------------------------|
| Frontend           | React.js             | Fast, reactive UI framework ideal for SPAs and real-time dashboards 
| Backend API        | Flask + Python       | Lightweight, easy-to-write APIs with rich ecosystem support (ML, Pandas, etc.)
| Database           | MongoDB              | Flexible NoSQL schema handles semi-structured cyber threat data well)
| ML Model           | ExtraTreesClassifier | Fast, robust ensemble model that handles high-dimensional TF-IDF vectors efficiently
| Feature Extraction | TF-IDF Vectorizer    | Converts text into sparse vectors, capturing term importance without deep learning overhead   
| Serialization      | Pickle               | Enables model saving/loading for seamless Flask API integration                              
| Containerization   | Docker + Compose     | Clean, reproducible, and platform-independent deployments


## 🗂️ Project Structure

```
ThreatDashboard/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── ingest.py              # Loads CSV into MongoDB
│   ├── train_model.py         # ML training (optional)
│   ├── requirements.txt       # Backend dependencies
│   └── Dockerfile
│
├── frontend/
│   ├── src/                   # React components
│   ├── package.json           # Frontend dependencies
│   └── Dockerfile
│
├── data/
│   └── cyber_threats.csv      # Source threat dataset
│
├── .env                       # MongoDB and CSV path config
├── docker-compose.yml         # Service orchestration
└── README.md
```

---

## 🚀 Getting Started (Local Docker)

### 1. Clone the repo

```
git clone <your-repo-url>
cd ThreatDashboard
```

### 2. Ensure `.env` contains:

```
MONGO_URI=mongodb://mongo:27017
DB_NAME=threatdb
COLLECTION_NAME=threats
CSV_PATH=/app/data/cyber_threats.csv
```

### 3. Build & Run all services

```
docker-compose up --build
```

This spins up:
- `mongo`: the database
- `backend`: Flask API on [localhost:5050](http://localhost:5050)
- `frontend`: React UI on [localhost:3000](http://localhost:3000)

---

## 📥 Load Sample Data

Inside the backend container, run:

```
docker-compose exec backend bash
python ingest.py
```

This imports `data/cyber_threats.csv` into MongoDB.

---

## 📊 How It Works

- **Backend (Flask)** handles:
  - `/api/threats` (list with filters)
  - `/api/threats/stats` (dashboard analytics)
  - `/api/analyze` (ML classification — WIP)

- **Frontend (React)** displays:
  - Dashboard with total threats, category/severity charts
  - Threats list with search, pagination

---

