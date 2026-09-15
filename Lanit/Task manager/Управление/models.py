from datetime import date, datetime
from sqlalchemy import ForeignKey, CheckConstraint, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from enum import Enum

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    status: Mapped[str] = mapped_column(default='todo')
    created_on: Mapped[date | None]
    due_on: Mapped[date | None]
    start_on: Mapped[date | None]
    completed_on: Mapped[date | None]
    updated_at: Mapped[datetime]
    priority: Mapped[str]
    project: Mapped[str]
    estimate_hours: Mapped[float | None]
    body: Mapped[str]
    extra: Mapped[dict] = mapped_column(JSON, default=dict)
    source_key: Mapped[str | None] = mapped_column(unique=True)
    __table_args__ = (CheckConstraint("status IN ('todo','doing','done')"),)

class Dependency(Base):
    __tablename__ = 'dependencies'
    prerequisite_id: Mapped[str] = mapped_column(ForeignKey('tasks.id'), primary_key=True)
    dependent_id: Mapped[str] = mapped_column(ForeignKey('tasks.id'), primary_key=True)
    __table_args__ = (CheckConstraint('prerequisite_id != dependent_id'),)


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "doing"
    DONE = "done"