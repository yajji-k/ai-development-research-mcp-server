from importlib import import_module
from unittest.mock import Mock

import app.tools.utility.uuid as uuid_tool


def test_get_uuid_tool_calls_service_and_returns_response_unchanged(monkeypatch):
    service = Mock()
    expected_response = object()
    service.get_uuid.return_value = expected_response
    monkeypatch.setattr(uuid_tool, "service", service)

    response = uuid_tool.get_uuid()

    service.get_uuid.assert_called_once_with()
    assert response is expected_response
