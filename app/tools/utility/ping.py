from app.telemetry.decorators import tool_execution
from app.services.utility.ping_service import PingService

service = PingService()

@tool_execution
def get_ping():
    """MCP tool adapter for ping."""
    return service.ping()

