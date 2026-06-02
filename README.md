# 🌸 Hangarin — Personal Task Manager

> *Hangarin* (Filipino): to wish, to aspire, to achieve.

Hangarin is a personal task management web app designed to help you organize your tasks, track your progress, and achieve your goals — all in one place.

---

## ✨ Features

- 🔐 **Authentication** — Register and log in with username/password, Google, or GitHub
- ✅ **Task Management** — Create, update, and delete tasks with priorities and categories
- 📋 **Sub Tasks** — Break down tasks into smaller, manageable subtasks
- 📝 **Notes** — Keep notes alongside your tasks
- 🏷️ **Categories & Priorities** — Organize tasks by category and priority level
- 📊 **Task Activity Dashboard** — Visual overview of your task activity over time
- 🔔 **Search** — Quickly find tasks with the search bar
- 📱 **Responsive Design** — Works on both desktop and mobile

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.0.6 |
| Auth | django-allauth (Google, GitHub OAuth) |
| Frontend | Bootstrap 5.3, Font Awesome 6.5 |
| Database | SQLite |
| Language | Python 3.11 |
| Deployment | PythonAnywhere |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/shenadp/Hangarin.git
cd Hangarin

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

Then visit `http://127.0.0.1:8000` in your browser.

---

## ⚙️ Environment Setup

For Google and GitHub OAuth to work, make sure to configure your Social Applications in the Django Admin panel (`/admin/`) with the correct Client ID and Secret Key from your Google Cloud Console and GitHub OAuth App settings.

---

## 📁 Project Structure

```
Hangarin/
├── config/          # Project settings and URLs
├── hangarin/        # Core app
├── taskmanager/     # Task, SubTask, Note, Category, Priority models
├── templates/       # HTML templates
├── static/          # Static files
└── manage.py
```

---

## 👩‍💻 Developer

Made with 💗 by **shenadp**
