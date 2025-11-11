"""Structured logging configuration with loguru."""

import sys
from pathlib import Path
from loguru import logger
from typing import Optional
from contextvars import ContextVar

# Context variables for structured logging
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)


def configure_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    structured: bool = True,
    rotation: str = "100 MB",
    retention: str = "1 month"
):
    """Configure loguru logging with structured output."""

    # Remove default handler
    logger.remove()

    # Define format
    if structured:
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level> | "
            "{extra}"
        )
    else:
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<level>{message}</level>"
        )

    # Console handler
    logger.add(
        sys.stderr,
        format=log_format,
        level=level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # File handler if specified
    if log_file:
        logger.add(
            log_file,
            format=log_format,
            level=level,
            rotation=rotation,
            retention=retention,
            compression="zip",
            backtrace=True,
            diagnose=True,
            enqueue=True,  # Thread-safe
        )

    logger.info(f"Logging configured at level {level}")


def get_logger(name: str):
    """Get a logger with context."""
    return logger.bind(
        module=name,
        request_id=request_id_var.get(),
        user_id=user_id_var.get(),
    )


def set_request_context(request_id: str, user_id: Optional[str] = None):
    """Set request context for logging."""
    request_id_var.set(request_id)
    if user_id:
        user_id_var.set(user_id)


def clear_request_context():
    """Clear request context."""
    request_id_var.set(None)
    user_id_var.set(None)
