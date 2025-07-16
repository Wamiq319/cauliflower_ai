# 🌿 Cauliflower AI – Disease Detection Platform

This is a Django-based AI platform that allows farmers to detect diseases in cauliflower crops using uploaded images. It includes separate dashboards for users (farmers), doctors (experts), and admins.

---

## 🚀 Project Structure

cauliflower_ai/
├── venv/ // Virtual environment
├── manage.py
├── db.sqlite3 // Local DB (SQLite for dev)
├── config/ // Django settings + URLs
├── apps/
│ ├── ui/ // Frontend templates and static files
│ ├── doctor/ // Logic/models for doctors
│ ├── user/ // Logic/models for farmers
│ └── core/ // Shared logic

## 🖥️ Frontend (UI App)

All UI templates and static files live under `apps/ui/`.

apps/ui/
├── static/
│ ├── css/
│ ├── image/
│ ├── img/
│ └── js/
└── templates/
├── base.html
├── landing.html
├── auth/
│ ├── login.html
│ └── register/
│ └── register_user.html
│ └── register_doctor.html
├── components/
│ ├── footer.html
│ └── navbar.html
└── dahboard/
├── dashboard_admin.html
├── dashboard_doctor.html
└── dashboard_user.html

Uses Tailwind CSS + daisyUI for styling.

## 🔧 Setup Instructions

# Clone the project

git clone <repo-url>
cd cauliflower_ai

# Create virtual environment

python -m venv venv
venv\Scripts\activate # or source venv/bin/activate (Linux/Mac)

# Install requirements

pip install -r requirements.txt

# Run migrations

python manage.py migrate

# Start dev server

python manage.py runserver

## 🧠 Roles and Dashboards

| Role   | Path              | Features                          |
| ------ | ----------------- | --------------------------------- |
| Farmer | /dashboard/user   | Upload image, see prediction      |
| Doctor | /dashboard/doctor | Review cases, give advice         |
| Admin  | /dashboard/admin  | Manage users and platform content |

## ✨ Contributors

- **Wamiq** – Frontend & Project Lead
- **Zryab Shakir** – AI & Backend Engineer

## 📄 License

This project is for educational and research use under university guidelines.
