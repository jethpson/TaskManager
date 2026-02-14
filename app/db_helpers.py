from . import db
from .models import User, Task
from datetime import datetime

# ---------------------------
# Database Initialization
# ---------------------------
def init_db(app, seed_sample_data=False):
    """
    Initialize the database tables.
    If seed_sample_data=True, creates a sample admin user and task.
    """
    with app.app_context():
        db.create_all()
        print("Database initialized!")

        if seed_sample_data:
            if not User.query.filter_by(username="admin").first():
                admin = User(username="admin", email="admin@example.com", role="admin")
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()
                print("Sample admin user created.")

                sample_task = Task(
                    title="Welcome Task",
                    description="This is your first task!",
                    assigned_user_id=admin.id,
                    due_date=datetime.utcnow(),
                    status="pending"
                )
                db.session.add(sample_task)
                db.session.commit()
                print("Sample task created.")

# ---------------------------
# User helpers
# ---------------------------
def create_user(username, email, password, role="user"):
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return None  # User already exists
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_all_users():
    return User.query.all()

# ---------------------------
# Task helpers
# ---------------------------
def add_task(title, description, assigned_user_id, due_date=None, status="pending"):
    task = Task(title=title, description=description, assigned_user_id=assigned_user_id, status=status)
    if due_date:
        task.due_date = due_date
    db.session.add(task)
    db.session.commit()
    return task

def get_task(task_id):
    return Task.query.get(task_id)

def update_task(task_id, **kwargs):
    task = get_task(task_id)
    if not task:
        return None
    for key, value in kwargs.items():
        if hasattr(task, key):
            setattr(task, key, value)
    db.session.commit()
    return task

def delete_task(task_id):
    task = get_task(task_id)
    if not task:
        return False
    db.session.delete(task)
    db.session.commit()
    return True

def get_tasks_for_user(user_id, status=None):
    query = Task.query.filter_by(assigned_user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    return query.all()