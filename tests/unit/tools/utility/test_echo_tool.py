from importlib import import_module
from unittest.mock import Mock
import app.tools.utility.echo as echo_tool

def test_get_echo_tool_calls_service_with_message_and_returns_response_unchanged(monkeypatch):
    message = "Hello MCP"
    service = Mock()
    expected_response = object()
    service.echo.return_value = expected_response
    monkeypatch.setattr(echo_tool, "service", service)

    response = echo_tool.get_echo(message)

    service.echo.assert_called_once_with(message=message)
    assert response is expected_response
