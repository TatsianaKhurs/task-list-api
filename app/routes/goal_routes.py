from flask import Blueprint, request
from app.models.goal import Goal
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