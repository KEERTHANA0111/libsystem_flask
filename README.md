# Library Management System (Python/Flask)

A production-ready, feature-rich Library Management System built with Python, Flask, and SQLAlchemy. This application supports two user roles: Administrators and Members (Students/Faculty).

## Features

- **Admin Dashboard**:
    - Real-time statistics (Total Books, Issued Books, Pending Requests).
    - Inventory Management (Add/Edit books).
    - Issue & Return tracking.
    - User directory.
- **Member Dashboard**:
    - Browse and search book inventory.
    - Submit procurement requests for new books.
    - View individual borrowing history.
- **Secure Authentication**:
    - Role-based login (Admin vs Member).
    - Password hashing using Werkzeug.
    - Session management via Flask-Login.
- **Modern UI**:
    - Responsive design using Bootstrap 5.
    - Interactive modals and icons.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone or download the project files.
2. Navigate to the project root directory:
    `cd library-management-system`
3. Install the required dependencies:
    `pip install -r requirements.txt`

## Running the Application

1. Open your terminal in the project directory.
2. Run the application:
    `python app.py`
3. The application will automatically create a local SQLite database file named `library.db` and seed a default administrator.
4. Access the application at:
    `http://127.0.0.1:5000`

## Initial Credentials

- **Administrator**:
    - **Username**: `admin`
    - **Password**: `password123`
- **Member**:
    - Register a new account via the **Register** link on the login page.

## Configuration

The application uses environment variables for sensitive settings. You can create a `.env` file or set them in your environment:

- `SECRET_KEY`: Custom secret for session signing.
- `DATABASE_URL`: Set this to use MySQL or PostgreSQL instead of SQLite (e.g., `mysql+pymysql://user:pass@localhost/db`).

## Project Structure

- `app.py`: Main application logic, routing, and controller functions.
- `models.py`: Database schema definitions using SQLAlchemy.
- `templates/`: HTML templates using Jinja2.
    - `base.html`: Common layout and navigation.
    - `login.html/register.html`: Auth pages.
    - `admin_dash.html`: Admin management interface.
    - `member_dash.html`: Personal member account view.
    - `search_books.html`: Catalog browsing interface.

## Troubleshooting

- **Database Errors**: If you encounter database errors after modifying `models.py`, delete the `instance/library.db` file and restart the app to regenerate the schema.
- **Missing Icons**: Ensure you have an internet connection to load Bootstrap and Bootstrap Icons from CDNs.
- **Login Issues**: Ensure you select the correct role (Admin/Member) from the dropdown during login.
