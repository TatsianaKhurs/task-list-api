from flask import Blueprint, request
from app.models.goal import Goal
from app.models.task import Task
from app.db import db
from app.route_utilities import validate_model


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


# Wave 5: Create a new goal
@goals_bp.post("")
def create_goal():
    request_body = request.get_json(silent=True)

    if not request_body or "title" not in request_body:
        return {"details": "Invalid data"}, 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return new_goal.to_dict(), 201


# Wave 5: Get all goals
@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = []

    for goal in goals:
        goals_response.append(goal.to_dict())

    return goals_response, 200


# Wave 5: Get one goal
@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(), 200


# Wave 5: Update a goal
@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}


# Wave 5: Delete a goal
@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}

# Wave 6: Associate tasks with a goal
@goals_bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    tasks = []

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        tasks.append(task)

    goal.tasks = tasks

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in tasks]
    }, 200

# Wave 6: Get all tasks belonging to a goal
@goals_bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []

    for task in goal.tasks:
        tasks_response.append(task.to_dict())

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }, 200