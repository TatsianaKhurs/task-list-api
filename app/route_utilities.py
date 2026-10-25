from flask import abort, make_response
from .db import db


def validate_model(model_class, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(400)

    query = db.select(model_class).where(model_class.id == model_id)
    model = db.session.scalar(query)

    if model is None:
        response = {"message": f"{model_class.__name__.lower()} {model_id} not found"}
        abort(make_response(response, 404))

    return model