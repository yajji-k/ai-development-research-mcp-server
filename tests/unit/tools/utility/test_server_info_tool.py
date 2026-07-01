from importlib import import_module
from unittest.mock import Mock

import app.tools.utility.server_info as server_info_tool


def test_get_server_info_tool_calls_service_and_returns_response_unchanged(monkeypatch):
    service = Mock()
    expected_response = object()
    service.get_server_info.return_value = expected_response
    monkeypatch.setattr(server_info_tool, "service", service)

    response = server_info_tool.get_server_info()

    service.get_server_info.assert_called_once_with()
    assert response is expected_response
