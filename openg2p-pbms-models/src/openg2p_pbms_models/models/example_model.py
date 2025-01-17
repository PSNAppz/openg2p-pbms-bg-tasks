import enum
from datetime import datetime

from openg2p_fastapi_common.models import BaseORMModel
from sqlalchemy import DateTime, Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import mapped_column


class TaskStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class BackgroundTask(BaseORMModel):
    __tablename__ = "background_tasks"

    id = mapped_column(Integer, primary_key=True, index=True)
    task_status = mapped_column(String, default=TaskStatus.PENDING)
    attempt_count = mapped_column(Integer, default=0)
    last_attempt_datetime = mapped_column(DateTime, nullable=True)
    identifier = mapped_column(String, index=True)
