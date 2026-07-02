import pytest

from app.exceptions import ApplicationError, MCPServerError
from app.telemetry.decorators import prompt_execution


def test_prompt_execution_returns_wrapped_result():
    expected_response = object()

    @prompt_execution
    def prompt():
        return expected_response

    response = prompt()

    assert response is expected_response


def test_prompt_execution_reraises_application_error():
    @prompt_execution
    def prompt():
        raise ApplicationError("Prompt failed")

    with pytest.raises(ApplicationError, match="Prompt failed"):
        prompt()


def test_prompt_execution_converts_unexpected_exception_to_mcp_server_error():
    @prompt_execution
    def prompt():
        raise RuntimeError("Unexpected failure")

    with pytest.raises(
        MCPServerError,
        match="Unexpected error while executing prompt 'prompt'",
    ):
        prompt()
