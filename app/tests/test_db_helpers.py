import pytest
from app import create_app, db
from app.models import User, Task
from app.db_helpers import create_user, get_user_by_username, add_task, get_task, update_task, delete_task
from datetime import datetime

@pytest.fixture
def app_instance():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def sample_user(app_instance):
    user = create_user("testuser", "test@example.com", "password123")
    return user

@pytest.fixture
def sample_task(app_instance, sample_user):
    task = add_task(
        title="Test Task",
        description="Task for testing",
        assigned_user_id=sample_user.id,
        due_date=datetime.utcnow(),
        status="pending"
    )
    return task

def test_create_and_get_user(app_instance):
    user = create_user("alice", "alice@example.com", "alicepass")
    fetched = get_user_by_username("alice")
    assert fetched is not None
    assert fetched.email == "alice@example.com"

def test_add_and_get_task(app_instance, sample_task):
    task = get_task(sample_task.id)
    assert task.title == "Test Task"
    assert task.status == "pending"

def test_update_task(app_instance, sample_task):
    updated = update_task(sample_task.id, title="Updated Task", status="completed")
    assert updated.title == "Updated Task"
    assert updated.status == "completed"

def test_delete_task(app_instance, sample_task):
    result = delete_task(sample_task.id)
    assert result is True
    assert get_task(sample_task.id) is None
