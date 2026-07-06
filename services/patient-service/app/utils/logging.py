import logging
import sys
from logging.handlers import RotatingFileHandler
from app.config.config import settings

def setup_logging():
    """
    Configure enterprise logging for the Patient Service.
    Logs to both stdout and a rolling file.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Define log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(process)d] - %(message)s'
    )

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler for persistence
    file_handler = RotatingFileHandler(
        "patient_service.log",
        maxBytes=10*1024*1024, # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logging.info(f"Logging initialized at level {settings.LOG_LEVEL}")

logger = logging.getLogger("patient-service")
