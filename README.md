# ORM AI Platform

AI based monitoring and face recognition platform using YOLO, deep learning embeddings, Dockerized microservices, and modern frontend architecture.

## Features

* Real time object detection using YOLOv8
* Face recognition with embedding extraction
* Deep learning based face classifier
* Multi service Docker architecture
* FastAPI backend services
* Vue.js frontend applications
* Dataset augmentation and training pipeline
* Video processing and face extraction
* REST API integration
* Responsive monitoring dashboard

---

# Project Structure

```bash
orm-project/
│
├── apps/
│   ├── face-recognition/
│   │   ├── backend/
│   │   └── frontend/
│   │
│   ├── orm-system/
│   │   ├── backend/
│   │   └── frontend/
│   │
│   └── landing-page/
│
├── docker-compose.yml
├── package.json
└── README.md
```

---

# Technologies

## Backend

* Python
* FastAPI
* TensorFlow
* InsightFace
* YOLOv8
* OpenCV

## Frontend

* Vue.js
* Vite
* TailwindCSS

## Deployment

* Docker
* Docker Compose

---

# Services

| Service       | Port |
| ------------- | ---- |
| Landing Page  | 8000 |
| ORM Frontend  | 8001 |
| Face Frontend | 8002 |
| ORM Backend   | 8080 |
| Face Backend  | 8090 |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/USERNAME/orm-ai-platform.git
cd orm-ai-platform
```

---

# Run with Docker

```bash
docker compose up --build
```

---

# Run Frontend Manually

```bash
npm install
npm run dev
```

---

# Run Backend Manually

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

---

# Face Recognition Pipeline

1. Extract frames from videos
2. Detect and crop faces
3. Augment dataset
4. Split train and validation dataset
5. Generate face embeddings
6. Train classifier model
7. Perform face recognition inference

---

# Models

This project uses:

* YOLOv8 for object detection
* Face embeddings for facial feature extraction
* Neural network classifier for identity recognition

---

# Docker Deployment

Start all services:

```bash
docker compose up -d
```

Stop all services:

```bash
docker compose down
```

Check running containers:

```bash
docker ps
```

---

# Notes

* Large AI model files may not be included in this repository
* Use Git LFS for large model storage
* node_modules and virtual environments are excluded from version control

---

# License

This project is developed for research and educational purposes.
