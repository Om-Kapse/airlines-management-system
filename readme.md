# ✈️ Airlines Management System (Django Project)

## 📌 Overview
A Database Management System project built using **Python Django**.  
It allows passengers to search flights, book tickets, cancel bookings, and view their booking history.  

## ⚙️ Tech Stack
- Python 3.12+
- Django 5.x
- SQLite (default)

## 🚀 Features
- User registration & login (Passenger, Staff, Admin roles)
- Flight management (staff/admin)
- Search & book flights
- Booking history
- Cancel booking
- Passenger dashboard with navigation bar

## 🔧 Setup Instructions
```bash
# 1. Clone repo
git clone https://github.com/Om-Kapse/airlines-management-system.git
cd airlines-management-system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start server
python manage.py runserver
