import logging
from datetime import datetime

import httpx
from openg2p_pbms_models.models import (
    BackgroundTask,
    TaskStatus
)
from sqlalchemy.orm import sessionmaker

from ..app import celery_app, get_engine
from ..config import Settings

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)
_engine = get_engine()

@celery_app.task(name="worker_task_name")
def worker_task(identifier):
    _logger.info(f"Worker processing identifier: {identifier}")
    Session = sessionmaker(bind=_engine, expire_on_commit=False)
    session = Session()

    task_record = None
    try:
        task_record = session.query(BackgroundTask).filter_by(identifier=identifier).first()
        if task_record:
            # Perform the main processing logic here...
            task_record.task_status = "COMPLETED"
            task_record.last_attempt_datetime = datetime.utcnow()
            session.commit()
    except Exception as e:
        if task_record:
            task_record.task_status = TaskStatus.FAILED
            task_record.last_attempt_datetime = datetime.utcnow()
            session.commit()
        _logger.error(f"Worker task failed for identifier: {identifier}, error: {str(e)}")
    finally:
        session.close()
