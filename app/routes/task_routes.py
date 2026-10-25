from flask import Blueprint, request
from app.models.task import Task
from app.models.task import Task
from app.db import db
from datetime import datetime

from app.route_utilities import validate_model

import requests
import os

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


# Wave 1: Create a new task
@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    if not request_body or "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

# Wave 1 and Wave 2: Get all tasks with sorting
@tasks_bp.get("")
def get_all_tasks():
    sort = request.args.get("sort")

    query = db.select(Task)

    if sort == "asc":
        query = query.order_by(Task.title.asc())

    elif sort == "desc":
        query = query.order_by(Task.title.desc())

    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)

    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())

    return tasks_response, 200

# Wave 1: Get one task
@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict(), 200

# Wave 1: Update a task
@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}

# Wave 1: Delete a task
@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}

# Wave 3: Mark a task incomplete
@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}

# Wave 3: Mark a task complete
@tasks_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"

    headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"
    }

    message = {
        "channel": os.environ.get("SLACK_CHANNEL_ID"),
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(url, json=message, headers=headers, timeout=10)

    return "", 204, {"Content-Type": "application/json"}