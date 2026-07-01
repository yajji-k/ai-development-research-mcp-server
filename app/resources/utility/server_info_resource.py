from fastmcp.resources import ResourceContent, ResourceResult

from app.telemetry.decorators import tool_execution
from app.services.utility.server_info_service import ServerInfoService

service = ServerInfoService()

@tool_execution
def server_info() -> ResourceResult:
    """MCP resource exposing server information."""
    response = service.get_server_info()
    return ResourceResult(
        [
            ResourceContent(
                response,
                mime_type="application/json",
            )
        ]
    )
