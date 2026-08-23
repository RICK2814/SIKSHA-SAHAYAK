# 🎓 SIKSHA SAHAYAK

> A futuristic Django-based learning and assessment platform that brings curriculum, study materials, practice, assessments, accounts, and learner progress into one intelligent learning ecosystem.

<p align="center">
  <a href="https://siksha-sahayak-zj9u.onrender.com">
    <img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=2" width="100%" alt="Live animated robotic Siksha Sahayak system console" />
  </a>
</p>

<p align="center">
  <a href="https://siksha-sahayak-zj9u.onrender.com"><strong>🚀 OPEN LIVE DEMO</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.2%2B-092E20?logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=111111" alt="Render" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT" />
</p>

> **Live deployment note:** hosted on Render's free tier. The service may need a short wake-up period after inactivity, and the current SQLite deployment is not intended as a durable production datastore.

---

## ✨ Overview

<div align="center">
  <img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=2" width="100%" alt="Animated robotic overview console" />
</div>

**Siksha Sahayak** is a structured digital-learning platform built with Django. It connects learner accounts, curriculum content, educational materials, practice flows, and assessments into a single application.

The experience is designed around a clear learning loop:

**Discover → Learn → Practice → Assess → Review → Improve**

---

## 🚀 Core Features

<div align="center">
  <img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=2" width="100%" alt="Animated robotic feature matrix" />
</div>

- 👤 **Learner Accounts** — registration, login, profiles, and authenticated workflows
- 📚 **Curriculum & Materials** — class, subject, chapter, and study-content organization
- 🧠 **Practice Experience** — question-based learning and revision workflows
- 📝 **Assessments** — attempts, scoring, results, and learner-facing assessment flows
- 🗂️ **Management Commands** — reusable data-seeding and curriculum-loading workflows
- 🌐 **Deployment Ready** — Gunicorn, WhiteNoise, Render-compatible configuration

---

## 🧱 Project Structure

<div align="center">
  <img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=2" width="100%" alt="Animated robotic architecture scan" />
</div>

```text
SIKSHA-SAHAYAK/
├── accounts/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── assessments/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── management/
│
├── materials/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── management/
│
├── assets/
│   └── ai-core.svg
│
├── manage.py
├── requirements.txt
├── build.sh
└── README.md
```

---

## 🛠️ Tech Stack

<div align="center">
  <img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=2" width="100%" alt="Animated robotic technology radar" />
</div>

| Layer | Technology |
|---|---|
| Backend | Django 4.2+ |
| Language | Python 3.x |
| Database | SQLite / PostgreSQL-ready dependencies |
| Static Assets | WhiteNoise |
| Application Server | Gunicorn |
| Media / Imaging | Pillow |
| Deployment | Render |
| Data Seeding | Django management commands |

---

## ⚙️ Local Setup

<div align="center">
  <img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=2" width="100%" alt="Animated robotic setup terminal" />
</div>

### 1. Clone

```bash
git clone https://github.com/RICK2814/SIKSHA-SAHAYAK.git
cd SIKSHA-SAHAYAK
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

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

### 5. Load project data

Use the available Django management commands under:

```text
materials/management/commands/
assessments/management/commands/
```

### 6. Start the server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

---

## 🔐 Configuration & Security

<div align="center">
  <img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=2" width="100%" alt="Animated robotic security monitor" />
</div>

Before production deployment, configure environment-specific values for:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- Database connection
- Static/media storage
- Production security settings

Never commit passwords, API keys, private tokens, or deployment credentials to GitHub.

---

## 🧩 Application Modules

<div align="center">
  <img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=2" width="100%" alt="Animated robotic module network" />
</div>

### `accounts`

User and learner account workflows including models, forms, URLs, views, and authentication-related functionality.

### `materials`

Curriculum and educational-material workflows, including models, views, routes, and management commands used to populate learning content.

### `assessments`

Assessment models, views, routing, management commands, learner attempts, scoring, and result flows.

---

## 📈 Future Scope

<div align="center">
  <img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=2" width="100%" alt="Animated robotic evolution engine" />
</div>

- 🤖 Personalized learning recommendations
- 📊 Learning analytics and progress dashboards
- 🔥 Progress streaks and learner motivation systems
- 🧪 More interactive question and assessment types
- 🧠 AI-assisted study support
- 👨‍🏫 Role-based student, teacher, and administrator dashboards
- 📱 REST API support for mobile or external clients
- ☁️ Production-grade monitoring and deployment automation

---

## 🤝 Contributing

<div align="center">
  <img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=2" width="100%" alt="Animated robotic collaboration console" />
</div>

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Test the application locally.
5. Commit with a clear message.
6. Open a pull request.

---

## 📄 License

<div align="center">
  <img src="https://raw.githubusercontent.com/RICK2814/SIKSHA-SAHAYAK/main/assets/ai-core.svg?v=2" width="100%" alt="Animated robotic open source core" />
</div>

This project is intended to be distributed under the **MIT License**.

---

## 🔗 Links

<div align="center">
  <a href="https://siksha-sahayak-zj9u.onrender.com"><strong>🌐 LIVE APPLICATION</strong></a>
  &nbsp; • &nbsp;
  <a href="https://github.com/RICK2814/SIKSHA-SAHAYAK"><strong>💻 GITHUB REPOSITORY</strong></a>
</div>

<p align="center">
  <sub>🤖 Every major README section is powered by the same live animated robotic console for a consistent futuristic visual system.</sub>
</p>
