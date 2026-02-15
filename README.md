# Task Manager Web Application

A full-stack **Task Management System** built with **Flask**, **SQLite**, and **JavaScript**.  
Supports user authentication, role-based access, and CRUD operations for tasks.

---

## Features

- RESTful API endpoints for **task management** and **user authentication**  
- Role-based authentication and input validation  
- SQLite database backend with efficient CRUD operations  
- Front-end integration using HTML5, CSS3, and JavaScript ES6  
- Unit and integration tests using **pytest**  
- Cross-platform: Windows, macOS, and Linux  

---

## Prerequisites

- Python 3.10+  
- `pip` (Python package manager)  
- Optional: `virtualenv` for isolated environments  

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/jethpson/TaskManager.git
cd TaskManager
```

### 2. Set up a virtual environment (recommended)

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root with:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///task_manager.db
```

> **Note:** `SECRET_KEY` is used for session management and security.

---

## Database Setup

Initialize the database with:

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> from app.db_helpers import init_db
>>> init_db(app, seed_sample_data=True)
>>> exit()
```

This will create the SQLite database and a sample admin user and task.

---

## Running the Application

### Linux / macOS

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

### Windows (PowerShell)

```powershell
$env:FLASK_APP="run.py"
$env:FLASK_ENV="development"
flask run
```

The app will be available at: `http://127.0.0.1:5000`

---

## Running Tests

Tests are written with **pytest**.

```bash
pytest -v
```

> Ensure your virtual environment is active before running tests.

---

## Optional: Deployment Notes

- Can be deployed using **Gunicorn** or **uWSGI** behind a **reverse proxy (Nginx/Apache)**  
- Use **environment variables** for production secrets  
- Consider migrating to **PostgreSQL or SQL Server** for production  

---

## Authors

- Jacob Thompson – [GitHub](https://github.com/jethpson/)

---

## Template Resources Used

[StartBootstrap Template GitHub](https://github.com/StartBootstrap/startbootstrap-sb-admin)

## License

This project is licensed under the MIT License.
