import app.tools.utility.ping as ping_tool
from unittest.mock import Mock


def test_get_ping_tool_calls_service_and_returns_response_unchanged(monkeypatch):
    service = Mock()
    expected_response = object()
    service.ping.return_value = expected_response
    monkeypatch.setattr(ping_tool, "service", service)

    response = ping_tool.get_ping()

    service.ping.assert_called_once_with()
    assert response is expected_response
