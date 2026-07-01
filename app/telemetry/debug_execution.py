import inspect
import logging
import warnings
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger(__name__)

_MAX_DEPTH = 6
_INSPECT_METHODS = ("model_dump", "model_dump_json", "dict")
_INSPECT_ATTRIBUTES = ("contents", "content", "mime_type")


def _safe_repr(value: Any) -> str:
    try:
        return repr(value)
    except Exception as exc:
        return f"<repr failed: {type(exc).__name__}: {exc}>"


def _log_method_result(value: Any, method_name: str, path: str) -> None:
    method = getattr(value, method_name, None)
    if not callable(method):
        return

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            method_result = method()
        logger.debug(
            "debug_execution return inspection %s.%s(): %r",
            path,
            method_name,
            method_result,
        )
    except Exception:
        logger.debug(
            "debug_execution return inspection %s.%s() failed",
            path,
            method_name,
            exc_info=True,
        )


def _log_nested_value(
    value: Any,
    *,
    path: str,
    depth: int = 0,
    seen: set[int] | None = None,
) -> None:
    if seen is None:
        seen = set()

    logger.debug(
        "debug_execution return inspection %s: type=%s repr=%s",
        path,
        type(value).__name__,
        _safe_repr(value),
    )

    if depth >= _MAX_DEPTH:
        logger.debug("debug_execution return inspection %s: max depth reached", path)
        return

    value_id = id(value)
    if value_id in seen:
        logger.debug("debug_execution return inspection %s: already inspected", path)
        return
    seen.add(value_id)

    for method_name in _INSPECT_METHODS:
        _log_method_result(value, method_name, path)

    for attr_name in _INSPECT_ATTRIBUTES:
        if hasattr(value, attr_name):
            try:
                attr_value = getattr(value, attr_name)
            except Exception:
                logger.debug(
                    "debug_execution return inspection %s.%s failed",
                    path,
                    attr_name,
                    exc_info=True,
                )
                continue

            logger.debug(
                "debug_execution return inspection %s.%s: type=%s repr=%s",
                path,
                attr_name,
                type(attr_value).__name__,
                _safe_repr(attr_value),
            )

    if isinstance(value, dict):
        for key, item in value.items():
            _log_nested_value(
                item,
                path=f"{path}[{key!r}]",
                depth=depth + 1,
                seen=seen,
            )
        return

    if isinstance(value, (list, tuple, set, frozenset)):
        for index, item in enumerate(value):
            _log_nested_value(
                item,
                path=f"{path}[{index}]",
                depth=depth + 1,
                seen=seen,
            )
        return

    nested_contents = getattr(value, "contents", None)
    if isinstance(nested_contents, (list, tuple)):
        for index, item in enumerate(nested_contents):
            _log_nested_value(
                item,
                path=f"{path}.contents[{index}]",
                depth=depth + 1,
                seen=seen,
            )


def debug_execution(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Temporarily log function inputs, return values, and nested resource payloads.
    """

    if inspect.iscoroutinefunction(fn):

        @wraps(fn)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.debug(
                "debug_execution before %s: args=%r kwargs=%r",
                fn.__name__,
                args,
                kwargs,
            )

            try:
                result = await fn(*args, **kwargs)
            except Exception:
                logger.exception("debug_execution exception in %s", fn.__name__)
                raise

            logger.debug(
                "debug_execution after %s: return_type=%s return_repr=%s",
                fn.__name__,
                type(result).__name__,
                _safe_repr(result),
            )
            _log_nested_value(result, path=f"{fn.__name__}.return")
            return result

        return async_wrapper

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.debug(
            "debug_execution before %s: args=%r kwargs=%r",
            fn.__name__,
            args,
            kwargs,
        )

        try:
            result = fn(*args, **kwargs)
        except Exception:
            logger.exception("debug_execution exception in %s", fn.__name__)
            raise

        logger.debug(
            "debug_execution after %s: return_type=%s return_repr=%s",
            fn.__name__,
            type(result).__name__,
            _safe_repr(result),
        )
        _log_nested_value(result, path=f"{fn.__name__}.return")
        return result

    return wrapper
