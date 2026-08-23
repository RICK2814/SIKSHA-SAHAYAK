# 🎓 SIKSHA SAHAYAK

> A futuristic Django-based learning and assessment platform that brings curriculum, study materials, practice, assessments, accounts, and learner progress into one intelligent learning ecosystem.

<p align="center"><a href="https://siksha-sahayak-zj9u.onrender.com"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=4" width="100%" alt="Live animated robotic Siksha Sahayak system console" /></a></p>

<p align="center"><a href="https://siksha-sahayak-zj9u.onrender.com"><strong>🚀 OPEN LIVE DEMO</strong></a></p>

<p align="center"><img src="https://img.shields.io/badge/Django-4.2%2B-092E20?logo=django&logoColor=white" alt="Django" /> <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite" /> <img src="https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=111111" alt="Render" /> <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT" /></p>

## ✨ Overview

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/overview-core.svg?v=1" width="100%" alt="Animated robotic overview core" /></p>

**Siksha Sahayak** is a structured digital-learning platform built with Django. It connects learner accounts, curriculum content, educational materials, practice flows, and assessments into a single application.

**Discover → Learn → Practice → Assess → Review → Improve**

## 🚀 Core Features

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/features-matrix.svg?v=1" width="100%" alt="Animated robotic feature matrix" /></p>

- 👤 Learner registration, login, profiles, and authentication
- 📚 Curriculum, class, subject, chapter, and material organization
- 🧠 Practice and question-bank workflows
- 📝 Assessments, attempts, scoring, and results
- 🗂️ Django data-seeding and management commands
- 🌐 Gunicorn, WhiteNoise, and Render deployment support

## 🧱 Project Structure

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/project-structure.svg?v=1" width="100%" alt="Animated robotic repository architecture scan" /></p>

```text
SIKSHA-SAHAYAK/
├── accounts/
├── assessments/
├── materials/
├── assets/
├── manage.py
├── requirements.txt
├── build.sh
└── README.md
```

## 🛠️ Tech Stack

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/tech-neural-radar.svg?v=1" width="100%" alt="Animated technology neural radar" /></p>

| Layer | Technology |
|---|---|
| Backend | Django 4.2+ |
| Language | Python 3.x |
| Database | SQLite / PostgreSQL-ready |
| Static Files | WhiteNoise |
| Application Server | Gunicorn |
| Image Handling | Pillow |
| Deployment | Render |

## ⚙️ Local Setup

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/local-setup-terminal.svg?v=1" width="100%" alt="Animated robotic local development terminal" /></p>

### 1. Clone
```bash
git clone https://github.com/RICK2814/SIKSHA-SAHAYAK.git
cd SIKSHA-SAHAYAK
```

### 2. Create environment
```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Migrate
```bash
python manage.py migrate
```

### 5. Seed data
Use the Django management commands under `materials/management/commands/` and `assessments/management/commands/`.

### 6. Run
```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## 🔐 Configuration & Security

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/security-monitor.svg?v=1" width="100%" alt="Animated robotic security monitor" /></p>

Configure secret key, debug mode, allowed hosts, database credentials, static/media storage, and production security settings before deployment.

Never commit passwords, API keys, private tokens, or deployment credentials.

## 🧩 Application Modules

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/module-network.svg?v=1" width="100%" alt="Animated robotic application module network" /></p>

### `accounts`
User and learner account workflows, forms, views, URLs, and authentication.

### `materials`
Curriculum, educational materials, views, routes, and content seeding.

### `assessments`
Assessment models, routing, attempts, scoring, results, and management commands.

## 📈 Future Scope

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/evolution-engine.svg?v=1" width="100%" alt="Animated robotic evolution engine" /></p>

- 🤖 Personalized learning recommendations
- 📊 Learning analytics and progress dashboards
- 🔥 Progress streaks
- 🧪 More interactive question types
- 🧠 AI-assisted study support
- 👨‍🏫 Role-based dashboards
- 📱 REST API support
- ☁️ Production monitoring and automation

## 🤝 Contributing

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/collaboration-console.svg?v=1" width="100%" alt="Animated robotic collaboration console" /></p>

1. Fork the repository.
2. Create a feature branch.
3. Implement changes.
4. Test locally.
5. Commit clearly.
6. Open a pull request.

## 📄 License

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/license-core.svg?v=1" width="100%" alt="Animated robotic open source license core" /></p>

This project is distributed under the **MIT License**.

## 🔗 Links

<p align="center"><a href="https://siksha-sahayak-zj9u.onrender.com"><strong>🌐 LIVE APPLICATION</strong></a> &nbsp; • &nbsp; <a href="https://github.com/RICK2814/SIKSHA-SAHAYAK"><strong>💻 GITHUB REPOSITORY</strong></a></p>

<p align="center"><sub>🤖 Every major README section now has its own dedicated animated SVG visual.</sub></p>
