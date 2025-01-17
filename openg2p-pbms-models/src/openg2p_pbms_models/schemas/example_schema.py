from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class QueueEnum(str, Enum):
    EXAMPLE_TASK_QUEUE = "example_task_queue"

class BackgroundTask(BaseModel):
    __tablename__ = "background_tasks"

    id = Optional[int]
    task_status = TaskStatus
    attempt_count = int
    last_attempt_datetime = Optional[datetime]
