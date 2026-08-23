# 🎓 Siksha Sahayak

> A Django-based learning and assessment platform designed to bring curriculum, study materials, practice, assessments, and learner accounts together in one place.

[![Django](https://img.shields.io/badge/Django-Framework-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Overview

**Siksha Sahayak** is a web application for structured digital learning. It combines learner accounts, educational materials, curriculum data, practice content, and assessments inside a Django project.

The project is organized to support a complete learning flow:

```text
Learner
   ↓
Account / Profile
   ↓
Curriculum & Study Materials
   ↓
Practice / Learning Activities
   ↓
Assessments
   ↓
Progress & Results
```

## 🚀 Core Features

- 👤 User account and authentication flow
- 📚 Curriculum and subject/material management
- 🧠 Practice and learning activities
- 📝 Assessment and quiz functionality
- 📊 Learner-focused assessment views and results
- 🗂️ Django management commands for curriculum/data seeding
- 🎨 Template-based web interface
- 🧩 Modular Django app structure for future expansion

## 🧱 Project Structure

```text
SIKSHA-SAHAYAK/
├── accounts/                 # User accounts and authentication
├── assessments/             # Assessments, quizzes and related logic
├── materials/               # Curriculum, study materials and content
├── templates/                # Web templates and UI pages
├── manage.py                 # Django management entry point
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django / Python |
| Database | Django ORM compatible database |
| Frontend | HTML, CSS, JavaScript, Django Templates |
| Application Modules | `accounts`, `materials`, `assessments` |
| Data Management | Django management commands |
| Version Control | Git + GitHub |

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/RICK2814/SIKSHA-SAHAYAK.git
cd SIKSHA-SAHAYAK
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS/Linux:

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

### 5. Seed project data

The repository includes management commands for loading curriculum and application data. Use the commands available in `materials/management/commands/` and `assessments/management/commands/` as required by your deployment/setup workflow.

### 6. Run the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## 🔐 Configuration

Before production deployment, configure environment-specific settings such as:

- Django secret key
- Debug mode
- Allowed hosts
- Database credentials
- Static/media storage
- Production security settings

Do not commit secrets, API keys, passwords, or production credentials to GitHub.

## 🧩 Application Modules

### `accounts`

Handles learner/user account functionality, including models, forms, URLs, views, and authentication-related workflows.

### `materials`

Provides curriculum and educational-material functionality, along with management commands for populating learning content.

### `assessments`

Contains assessment models, views, routes, management commands, and learner-facing assessment workflows.

## 📈 Future Scope

- Personalized learning recommendations
- Learning analytics dashboard
- Progress tracking and streaks
- More interactive question types
- AI-assisted study support
- Role-based dashboards for students, teachers, and administrators
- REST API for mobile/front-end clients
- Production-grade monitoring and deployment automation

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the application locally.
5. Commit your changes with a clear message.
6. Open a pull request.

## 📄 License

This project is distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

## 🔗 Repository

**GitHub:** https://github.com/RICK2814/SIKSHA-SAHAYAK
