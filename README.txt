📚 Library Management System
A full-stack web application built with Flask and MySQL for managing library operations including book inventory, member borrowing history, and automated book requests.

🛠️ Tech Stack
Backend: Python Flask
Database: MySQL (via Flask-SQLAlchemy)
Frontend: Bootstrap 5, Jinja2 Templates
Authentication: Flask-Login & Werkzeug Security
🚀 Getting Started
1. Prerequisites
Python 3.9+
MySQL Server installed and running.
A MySQL GUI (like MySQL Workbench).
2. Installation
Clone the repository (or copy the project files).
Install dependencies:
 copy
bash

pip install flask flask-sqlalchemy flask-login pymysql cryptography
3. Database Configuration
Open MySQL Workbench and create the database:
 copy
sql

CREATE DATABASE library_db;
Update the connection string in app.py:
 copy
python

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:PASSWORD@localhost/library_db'
4. Create Tables
Run the following command in your terminal to generate the schema:

 copy
bash

python -c "from app import app, db; app.app_context().push(); db.create_all()"
Note: If icons do not appear in MySQL Workbench immediately, right-click "Tables" and select Refresh All.

📖 Features
Admin Module
Dashboard: Real-time stats on total books and pending requests.
Inventory: Full CRUD (Create, Read, Update, Delete) for books.
Circulation: Manually issue books to members and track return dates.
Member Management: Track and view student/faculty details.
Member Module
Search System: Filter the library catalog by Book Title or Author.
Request Facility: Submit requests for books not currently in the inventory.
Personal Profile: View active borrowed books and account details.
📂 Project Structure
 copy
text

├── app.py              # Main application logic & routes
├── models.py           # SQLAlchemy Database Models
├── extensions.py       # Shared DB instance
├── static/             # CSS, Images, and uploaded profile pics
├── templates/          # Jinja2 HTML layouts
│   ├── base.html       # Parent template
│   ├── admin_dash.html # Admin control panel
│   └── member_dash.html# Member profile page
└── requirements.txt    # List of dependencies
🚦 Running the App
Start the Flask server:
 copy
bash

python app.py
Open your browser and go to: http://127.0.0.1:5000
⚠️ Troubleshooting
Table reflection: If Workbench doesn't show tables after running db.create_all(), ensure you have selected USE library_db; in your SQL query tab.
Admin Access: For the first-time setup, manually add an admin record to the admin table via SQL or through a temporary registration route.
