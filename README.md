# 🤖 SIKSHA SAHAYAK

> A futuristic Django-based learning and assessment platform that brings curriculum, study materials, practice, assessments, accounts, and learner progress into one intelligent learning ecosystem.

<p align="center">
  <a href="https://siksha-sahayak-zj9u.onrender.com"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Live animated robotic Siksha Sahayak system console" /></a>
</p>

<p align="center"><a href="https://siksha-sahayak-zj9u.onrender.com"><strong>🚀 OPEN LIVE DEMO</strong></a></p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.2%2B-092E20?logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=111111" alt="Render" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT" />
</p>

## ✨ Overview

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Animated robotic overview console" /></p>

**Siksha Sahayak** is a web application for structured digital learning. It combines learner accounts, educational materials, curriculum data, practice content, assessments, and learner workflows inside a Django project.

## 🚀 Core Features

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Animated robotic feature console" /></p>

- Learner registration and authentication
- Curriculum and subject organization
- Study materials and learning resources
- Practice and question-bank workflows
- Online assessments and scoring
- Attempt/result tracking
- Django management commands for curriculum and data seeding
- Render-ready deployment configuration

## 🧱 Project Structure

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Animated robotic project structure console" /></p>

```text
SIKSHA-SAHAYAK/
├── accounts/                 # User accounts and authentication
├── assessments/              # Assessment models, views and workflows
├── materials/                # Curriculum, materials and learning content
├── assets/                   # Animated SVG visuals and project assets
├── manage.py
├── requirements.txt
├── build.sh
└── README.md
```

## 🛠️ Tech Stack

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Animated robotic technology console" /></p>

| Layer | Technology |
|---|---|
| Backend | Django 4.2+ |
| Language | Python 3.x |
| Database | SQLite / PostgreSQL-ready |
| Static Files | WhiteNoise |
| Production Server | Gunicorn |
| Hosting | Render |
| Image Handling | Pillow |

## ⚙️ Local Setup

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Animated robotic setup console" /></p>

### 1. Clone

```bash
git clone https://github.com/RICK2814/SIKSHA-SAHAYAK.git
cd SIKSHA-SAHAYAK
```

### 2. Create a virtual environment

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

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Seed data

Use the available management commands under `materials/management/commands/` and `assessments/management/commands/` according to the desired setup workflow.

### 6. Run locally

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## 🔐 Configuration

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Animated robotic configuration console" /></p>

Before production deployment, configure environment-specific values such as:

- Django secret key
- Debug mode
- Allowed hosts
- Database credentials
- Static/media storage
- Production security settings

Never commit passwords, API keys, secret keys, or production credentials.

## 🧩 Application Modules

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Animated robotic application module console" /></p>

### `accounts`

Learner/user account functionality, including models, forms, URLs, views, registration, login, and profile-related workflows.

### `materials`

Curriculum and educational-material functionality, including learning content and data-seeding commands.

### `assessments`

Assessment models, routes, views, question flows, attempts, scoring, and results.

## 📈 Future Scope

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Animated robotic future roadmap console" /></p>

- Personalized learning recommendations
- Learning analytics and progress dashboards
- Progress tracking and streaks
- More interactive question types
- AI-assisted study support
- Role-based student, teacher, and administrator dashboards
- REST API for mobile/front-end clients
- Production-grade monitoring and deployment automation

## 🤝 Contributing

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Animated robotic contribution console" /></p>

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the application locally.
5. Commit with a clear message.
6. Open a pull request.

## 📄 License

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Animated robotic license console" /></p>

This project is distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

## 🔗 Links

<p align="center"><img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=3" width="100%" alt="Animated robotic links console" /></p>

- **Live Demo:** https://siksha-sahayak-zj9u.onrender.com
- **GitHub:** https://github.com/RICK2814/SIKSHA-SAHAYAK
