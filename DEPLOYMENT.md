# 🚀 Deployment Guide - Argument Structure Analyzer

Anleitung zum Deployen der Web-App auf verschiedenen Plattformen.

---

## 📋 Inhaltsverzeichnis

1. [Lokales Development](#lokales-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
   - [Heroku](#heroku)
   - [AWS](#aws)
   - [Google Cloud](#google-cloud)
   - [Railway](#railway)
4. [Production Checklist](#production-checklist)
5. [Troubleshooting](#troubleshooting)

---

## 🖥️ Lokales Development

### Requirement
- Python 3.8+
- Docker (optional, aber empfohlen)

### Setup

#### Option A: Direkter Python Start
```bash
# 1. Repository klonen
git clone https://github.com/yourusername/argument_analyzer.git
cd argument_analyzer

# 2. Virtual Environment erstellen
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# oder
.venv\Scripts\activate     # Windows

# 3. Dependencies installieren
pip install -r requirements.txt

# 4. Streamlit App starten
streamlit run app.py
```

Die App läuft dann auf: **http://localhost:8501**

#### Option B: Docker Compose (empfohlen)
```bash
# 1. Repository klonen
git clone https://github.com/yourusername/argument_analyzer.git
cd argument_analyzer

# 2. Docker Compose starten
docker-compose up

# 3. Im Browser öffnen
# http://localhost:8501
```

**Vorteil:** Isolierte Umgebung, keine Python-Dependencies auf dem Host

### Entwicklung
```bash
# Änderungen spiegeln sich live auf http://localhost:8501
# Streamlit hat Auto-Reload aktiviert
```

---

## 🐳 Docker Deployment

### Lokales Docker Image bauen

```bash
# 1. Image bauen
docker build -t argument-analyzer:latest .

# 2. Container starten
docker run -p 8501:8501 argument-analyzer:latest

# 3. Im Browser öffnen
# http://localhost:8501
```

### Image Push zu Docker Hub

```bash
# 1. Bei Docker Hub anmelden
docker login

# 2. Tag erstellen (with your username)
docker tag argument-analyzer:latest yourusername/argument-analyzer:latest

# 3. Push
docker push yourusername/argument-analyzer:latest

# 4. Von überall pullen
docker run -p 8501:8501 yourusername/argument-analyzer:latest
```

---

## ☁️ Cloud Deployment

### 🔴 Heroku (einfach & kostenlos*)

**Heroku ist perfekt für schnelle Deployments.**

#### Voraussetzungen
- [Heroku Account](https://heroku.com)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

#### Deployment

```bash
# 1. Heroku login
heroku login

# 2. Heroku App erstellen
heroku create your-app-name

# 3. Git remote hinzufügen (falls noch nicht geschehen)
git remote add heroku https://git.heroku.com/your-app-name.git

# 4. Heroku spezifische Config (Procfile bereits vorhanden?)
# Falls nicht, erstelle Procfile:
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# 5. Git Push zu Heroku
git push heroku main

# 6. App öffnen
heroku open
```

**Logs anschauen:**
```bash
heroku logs --tail
```

**App scale:**
```bash
heroku ps:scale web=1
```

#### Kosten
- Free tier: 550 Dyno-Stunden/Monat (kostenlos)
- Paid tier: ab $7/Monat (unlimited)

---

### 🟦 Railway (GitHub Integration)

**Railway ist ideal für GitHub Integration & einfaches Deployment.**

#### Deployment

1. **Repository zu GitHub pushen**
```bash
git remote add origin https://github.com/yourusername/argument_analyzer.git
git push origin main
```

2. **Railway.app verbinden**
   - Gehe zu [railway.app](https://railway.app)
   - "New Project" → "Deploy from GitHub"
   - Wähle dein Repository
   - Railway erkennt Python automatisch
   - Deploy!

3. **Auto-Deploy aktivieren**
   - Jedes Git Push triggert automatisches Deployment
   - Logs & Metriken auf Railway Dashboard

#### Railway Konfiguration

Sollte automatisch funktionieren, aber falls nicht:

```yaml
# railway.json (optional, falls nötig)
{
  "buildCommand": "pip install -r requirements.txt",
  "startCommand": "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"
}
```

---

### 🟨 AWS (Elastic Beanstalk / ECS)

#### ECS + ECR (Docker)

```bash
# 1. AWS CLI Setup
aws configure

# 2. ECR Repository erstellen
aws ecr create-repository --repository-name argument-analyzer

# 3. Docker Image bauen & pushen
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker build -t argument-analyzer:latest .
docker tag argument-analyzer:latest <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/argument-analyzer:latest
docker push <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/argument-analyzer:latest

# 4. ECS Task Definition erstellen (via AWS Console)
# 5. ECS Service deployen
```

#### Elastic Beanstalk (einfacher)

```bash
# 1. Elastic Beanstalk CLI installieren
pip install awsebcli

# 2. Init
eb init -p python-3.11 argument-analyzer

# 3. Environment erstellen
eb create production

# 4. Deploy
git push

# 5. App öffnen
eb open
```

---

### 🟢 Google Cloud (Cloud Run)

**Cloud Run ist ideal für Serverless Deployment.**

```bash
# 1. Google Cloud CLI installieren
curl https://sdk.cloud.google.com | bash

# 2. Authenticieren
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 3. Image zu Artifact Registry pushen
gcloud auth configure-docker us-central1-docker.pkg.dev

docker build -t us-central1-docker.pkg.dev/YOUR_PROJECT_ID/argument-analyzer/app:latest .
docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/argument-analyzer/app:latest

# 4. Cloud Run Deploy
gcloud run deploy argument-analyzer \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/argument-analyzer/app:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 3600

# 5. Service URL wird angezeigt
```

---

## ✅ Production Checklist

Bevor du in Production gehst:

- [ ] **Environment Variables**
  ```bash
  # .env (nicht in Git committen!)
  DEBUG=false
  STREAMLIT_SERVER_HEADLESS=true
  STREAMLIT_SERVER_ENABLEXSRFPROTECTION=true
  ```

- [ ] **Secrets Management**
  - Keine API Keys in Code/Konfiguration
  - Nutze Platform-Secrets (Heroku, Railway, AWS, etc.)

- [ ] **Monitoring & Logging**
  ```bash
  # Performance Monitoring
  # Nutze Platform-Monitoring (Heroku Metrics, CloudWatch, etc.)
  ```

- [ ] **CORS & Security**
  ```python
  # app.py bereits sicher konfiguriert
  # Aber überprüfe für deine Domain:
  ```

- [ ] **Database (optional für Zukunft)**
  - Falls du Analyse-History speichern möchtest
  - PostgreSQL, MongoDB optional hinzufügen

- [ ] **Rate Limiting**
  - Optional: Streamlit Authenticator für Zugriffskontrolle

- [ ] **Backups & Recovery**
  - Platform-spezifische Backups aktivieren

---

## 🐛 Troubleshooting

### Streamlit Port-Fehler
```bash
# Wenn Port 8501 belegt ist
streamlit run app.py --server.port=8502
```

### Docker Build fehlt Abhängigkeiten
```bash
# Docker-Cache clearen
docker build --no-cache -t argument-analyzer:latest .
```

### Memory Fehler bei großen Texten
```bash
# Docker Memory erhöhen
docker run -p 8501:8501 -m 2g argument-analyzer:latest

# Oder in docker-compose.yml:
services:
  argument-analyzer:
    mem_limit: 2g
```

### Streamlit nicht erreichbar
```bash
# Firewall öffnen
# Heroku: sollte automatisch
# AWS: Security Group Port 8501 erlauben
# Docker: Port-Mapping überprüfen
```

---

## 📊 Performance Optimierung (zukünftig)

```python
# Caching für häufige Analysen
import streamlit as st

@st.cache_resource
def load_models():
    return TextPreprocessor()

# Lazy Loading für große Datasets
@st.cache_data
def load_test_cases():
    return list_test_cases()
```

---

## 🔗 Links & Ressourcen

- [Streamlit Deployment Docs](https://docs.streamlit.io/knowledge-base/tutorials/deploy)
- [Heroku Python Buildpack](https://github.com/heroku/heroku-buildpack-python)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Railway Docs](https://docs.railway.app)
- [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)
- [Google Cloud Run](https://cloud.google.com/run/docs)

---

**Glückliches Deploying! 🚀**
