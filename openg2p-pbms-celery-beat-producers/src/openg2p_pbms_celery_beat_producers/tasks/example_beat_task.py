import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from ..app import celery_app, get_engine
from ..config import Settings

from openg2p_pbms_models.models import BackgroundTask, TaskStatus, QueueEnum
from openg2p_pbms_models.schemas import TaskStatus, QueueEnum


_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)
_engine = get_engine()


@celery_app.task(name="example_beat_producer")
def example_beat_producer():
    _logger.info("Generic beat producer task executed")

    # Replace with your actual Session maker
    Session = sessionmaker(bind=_engine, expire_on_commit=False)

    with Session() as session:
        # Update entries exceeding max attempts
        session.query(BackgroundTask).filter(
            BackgroundTask.task_status == TaskStatus.PENDING,
            BackgroundTask.attempt_count >= _config.example_task_attempts,
        ).update(
            {
                BackgroundTask.task_status: TaskStatus.FAILED,
                BackgroundTask.last_attempt_datetime: datetime.utcnow(),
            },
            synchronize_session=False,
        )
        session.commit()

        # Select entries still pending and within attempts limit
        pending_entries = (
            session.execute(
                select(BackgroundTask)
                .filter(
                    BackgroundTask.task_status == TaskStatus.PENDING,
                    BackgroundTask.attempt_count < _config.example_task_attempts,
                )
                .limit(_config.batch_size)
            )
            .scalars()
            .all()
        )

        # Queue tasks with dynamic queue selection
        for entry in pending_entries:
            _logger.info(f"Queueing task for identifier: {entry.identifier}")
            celery_app.send_task(
                "example_worker_task",
                args=(entry.identifier,),
                queue=QueueEnum.EXAMPLE_TASK_QUEUE.value,
            )

    _logger.info("Completed checking for pending tasks")
