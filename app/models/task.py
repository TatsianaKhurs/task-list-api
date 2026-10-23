from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
        default=None
    )