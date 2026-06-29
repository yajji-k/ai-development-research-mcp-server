import logging

from app.config.settings import get_settings


def configure_logging() -> None:
    """
    Configure the application's logging
    """

    settings = get_settings()

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
