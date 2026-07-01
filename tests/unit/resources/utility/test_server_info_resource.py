from unittest.mock import Mock

from fastmcp.resources import ResourceResult

import app.resources.utility.server_info_resource as server_info_resource
from app.schemas.utility.server_info import ServerInfoResponse


def test_server_info_calls_service_and_returns_json_resource(monkeypatch):
    service = Mock()
    response_model = ServerInfoResponse(
        server_name="MCP Server",
        server_version="0.1.0",
        python_version="3.13.14",
        log_level="INFO",
        transport="stdio",
    )
    service.get_server_info.return_value = response_model
    monkeypatch.setattr(server_info_resource, "service", service)

    response = server_info_resource.server_info()

    service.get_server_info.assert_called_once_with()
    assert isinstance(response, ResourceResult)
    assert response.contents[0].content == response_model.model_dump_json()
    assert response.contents[0].mime_type == "application/json"
