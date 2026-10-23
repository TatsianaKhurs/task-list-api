from flask import abort
from .db import db


def validate_model(model_class, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(400)

    query = db.select(model_class).where(model_class.id == model_id)
    model = db.session.scalar(query)

    if model is None:
        abort(404)

    return model