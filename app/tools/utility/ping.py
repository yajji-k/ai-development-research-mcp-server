from app.services.utility.ping_service import PingService

service = PingService()

def ping():
    """MCP tool adapter for ping."""
    return service.ping()

