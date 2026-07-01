from app.telemetry.decorators import tool_execution
from app.services.utility.server_info_service import ServerInfoService

service = ServerInfoService()

@tool_execution
def get_server_info():
    """MCP tool for getting server_info"""
    return service.get_server_info()