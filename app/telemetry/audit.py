import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class AuditLogger:
    """
    Dedicated logger for audit events.
    """

    def __init__(self) -> None:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        self._logger = logging.getLogger("audit")
        self._logger.setLevel(logging.INFO)

        if not self._logger.handlers:
            handler = RotatingFileHandler(
                filename=log_dir / "audit.log",
                maxBytes=5 * 1024 * 1024,
                backupCount=5,
                encoding="utf-8",
            )

            formatter = logging.Formatter(
                "%(asctime)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._logger.propagate = False

    def log_tool_execution(
        self,
        tool_name: str,
        status: str,
        duration_ms: float,
        user: str = "anonymous",
    ) -> None:
        self._logger.info(
            "TOOL_EXECUTION | user=%s | tool=%s | status=%s | duration_ms=%.2f",
            user,
            tool_name,
            status,
            duration_ms,
        )
        
    def log_resource_access(
        self,
        resource_name: str,
        status: str,
        duration_ms: float,
        user: str = "anonymous",
    ) -> None:
        self._logger.info(
            "RESOURCE_ACCESS | user=%s | resource=%s | status=%s | duration_ms=%.2f",
            user,
            resource_name,
            status,
            duration_ms,
        )
        
    def log_prompt_execution(
        self,
        prompt_name: str,
        status: str,
        duration_ms: float,
        user: str = "anonymous",
    ) -> None:
        self._logger.info(
            "PROMPT_EXECUTION | user=%s | prompt=%s | status=%s | duration_ms=%.2f",
            user,
            prompt_name,
            status,
            duration_ms,
        )

    def log_authentication(
        self,
        user: str,
        status: str,
    ) -> None:
        self._logger.info(
            "AUTHENTICATION | user=%s | status=%s",
            user,
            status,
        )

    def log_server_event(self, event: str) -> None:
        self._logger.info(
            "SERVER | event=%s",
            event,
        )


audit_logger = AuditLogger()