import logging
import time
from functools import wraps
from typing import Any, Callable

from app.exceptions import ApplicationError, MCPServerError

logger = logging.getLogger(__name__)


def tool_execution(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Log tool execution, measure execution time and normalize unexpected errors.
    """

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        logger.info("Executing tool '%s'", fn.__name__)

        try:
            result = fn(*args, **kwargs)
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.info(
                "Tool '%s' completed successfully in %.2f ms",
                fn.__name__,
                duration_ms,
            )
            return result

        except MCPServerError:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.warning(
                "Tool '%s' failed in %.2f ms",
                fn.__name__,
                duration_ms,
                exc_info=True,
            )
            raise

        except Exception as exc:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                "Unexpected error while executing tool '%s' in %.2f ms",
                fn.__name__,
                duration_ms,
            )
            raise ApplicationError(
                "An unexpected internal error occurred."
            ) from exc

    return wrapper