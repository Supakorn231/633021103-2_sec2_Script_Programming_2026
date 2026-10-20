import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def setup_logging(name, level=logging.INFO):
    """Create and configure a logger for a module."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def ensure_directory_exists(path):
    """Create a directory if it does not already exist."""
    if not path:
        return
    try:
        os.makedirs(path, exist_ok=True)
        logging.info("Directory ensured: %s", path)
    except OSError as error:
        logging.error("Error creating directory %s: %s", path, error)
        raise
