from flask import abort, make_response, jsonify
from .db import db


def validate_model(model_class, model_id):
    try:
        model_id = int(model_id)
    except (ValueError, TypeError):
        abort(400)

    query = db.select(model_class).where(model_class.id == model_id)
    model = db.session.scalar(query)

    if model is None:
        response = {
            "message": f"{model_class.__name__.lower()} {model_id} not found"
        }
        abort(make_response(response, 404))

    return model


def create_model(model_class, request_body):
    if not request_body or "title" not in request_body:
        response = jsonify({"details": "Invalid data"})
        response.status_code = 400
        abort(response)

    if model_class.__name__ == "Task" and "description" not in request_body:
        response = jsonify({"details": "Invalid data"})
        response.status_code = 400
        abort(response)

    new_model = model_class.from_dict(request_body)

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201