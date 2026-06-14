# 💰 Personal Finance Management Dashboard

A modern, responsive Django-based web application designed to help individuals track their income, manage expenses, set budgets, and monitor savings goals.

---

## 🌟 Key Features

* **Income Tracking**: Log income from various sources with custom descriptions and dates.
* **Expense Management**: Categorize expenses (Housing, Food, Utilities, Shopping, Entertainment, etc.) to understand spending habits.
* **Budget Planning**: Set monthly budgets for specific categories and monitor spending against limit thresholds.
* **Savings Goals**: Set target savings goals with deadlines and visualize your progress as you save.
* **User Authentication**: Secure user registration, login, and logout. Data is isolated per user.
* **Modern UI**: Sleek, clean, and intuitive responsive dashboard design.

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites
* Python 3.8 or higher
* Git

### Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   git clone https://github.com/keerthana2625/finance_dashboard.git
   cd finance_dashboard
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser** (optional, for accessing the Django Admin panel):
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 🛠️ Built With

* **Backend**: Django (Python)
* **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
* **Database**: SQLite3 (Default, easily configurable for PostgreSQL/MySQL)

---

## 📂 Project Structure

```text
├── finance_dashboard/     # Django project configuration
├── financeapp/            # Django app for core finance logic (models, views, templates)
├── templates/             # HTML templates for the dashboard, login, and trackers
├── static/                # CSS, JavaScript, and asset files
├── manage.py              # Django command-line utility
└── requirements.txt       # Project dependencies
```
