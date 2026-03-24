# utils/logger.py
# =====================
# Centralized logging configuration.
# Provides a configured logger instance for the framework.

import logging
import sys


def get_logger(name: str = "framework", level: int = logging.INFO) -> logging.Logger:
    """
    Get a configured logger instance.

    :param name: Logger name (usually __name__ of the calling module)
    :param level: Logging level (default: INFO)
    :return: Configured Logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        logger.setLevel(level)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
