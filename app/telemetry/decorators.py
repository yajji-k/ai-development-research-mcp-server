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


def resource_execution(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Log resource execution, measure execution time and normalize unexpected errors.
    """

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        logger.info("Executing resource '%s'", fn.__name__)

        try:
            result = fn(*args, **kwargs)
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.info(
                "Resource '%s' completed successfully in %.2f ms",
                fn.__name__,
                duration_ms,
            )
            return result

        except MCPServerError:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.warning(
                "Resource '%s' failed in %.2f ms",
                fn.__name__,
                duration_ms,
                exc_info=True,
            )
            raise

        except Exception as exc:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                "Unexpected error while executing resource '%s' in %.2f ms",
                fn.__name__,
                duration_ms,
            )
            raise ApplicationError(
                "An unexpected internal error occurred."
            ) from exc

    return wrapper


def prompt_execution(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Log prompt execution, measure execution time and normalize unexpected errors.
    """

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        prompt_name = fn.__name__
        start_time = time.perf_counter()

        logger.info("Executing prompt '%s'", prompt_name)

        try:
            result = fn(*args, **kwargs)

            execution_time = (time.perf_counter() - start_time) * 1000

            logger.info(
                "Prompt '%s' completed successfully in %.2f ms",
                prompt_name,
                execution_time,
            )

            return result

        except ApplicationError:
            raise

        except Exception as exc:
            logger.exception(
                "Unexpected error while executing prompt '%s'",
                prompt_name,
            )
            raise MCPServerError(
                f"Unexpected error while executing prompt '{prompt_name}'"
            ) from exc

    return wrapper

