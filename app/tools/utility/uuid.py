from app.telemetry.decorators import tool_execution
from app.services.utility import UUIDService

service = UUIDService()

@tool_execution
def get_uuid():
    """Generate a new UUID version 4."""
    return service.get_uuid()