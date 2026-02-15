import pytest
from app import create_app, db
from app.models import User, Task
from datetime import datetime

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_register_user(client):
    res = client.post('/users/register', json={
        "username": "apiuser",
        "email": "api@example.com",
        "password": "password123"
    })
    data = res.get_json()
    assert res.status_code == 201
    assert "created successfully" in data['message']
