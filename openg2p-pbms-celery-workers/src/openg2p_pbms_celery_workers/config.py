from openg2p_fastapi_common.config import Settings as BaseSettings
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="pbms_celery_workers_", env_file=".env", extra="allow"
    )
    openapi_title: str = "OpenG2P PBMS Celery Workers"
    openapi_description: str = """
        Celery workers for OpenG2P PBMS
        ***********************************
        Further details goes here
        ***********************************
        """
    openapi_version: str = __version__

    db_dbname: str = "pbmsdb"
    db_driver: str = "postgresql"

    celery_broker_url: str = "redis://localhost:6379/0"
    celery_backend_url: str = "redis://localhost:6379/0"

    example_worker_task_attempts: int = 3


