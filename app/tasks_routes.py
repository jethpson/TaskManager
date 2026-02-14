from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from . import db
from .models import Task
from datetime import datetime

# Blueprint for task-related routes
tasks_bp = Blueprint('tasks', __name__)

# -------------------------
# Task Endpoints
# -------------------------
@tasks_bp.route('/', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(assigned_user_id=current_user.id).all()
    return jsonify({'tasks': [t.to_dict() for t in tasks]})

@tasks_bp.route('/', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    due_date = data.get('due_date')
    status = data.get('status', 'pending')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    task = Task(
        title=title,
        description=description,
        status=status,
        assigned_user_id=current_user.id
    )

    if due_date:
        try:
            task.due_date = datetime.fromisoformat(due_date)
        except ValueError:
            return jsonify({'error': 'Invalid due_date format'}), 400

    db.session.add(task)
    db.session.commit()
    return jsonify({'task': task.to_dict()}), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.assigned_user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)

    due_date = data.get('due_date')
    if due_date:
        try:
            task.due_date = datetime.fromisoformat(due_date)
        except ValueError:
            return jsonify({'error': 'Invalid due_date format'}), 400

    db.session.commit()
    return jsonify({'task': task.to_dict()})

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.assigned_user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

@tasks_bp.route('/new', methods=['GET'])
@login_required
def new_task_page():
    return render_template('task_form.html')