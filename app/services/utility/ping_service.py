from app.schemas.utility.ping import PingResponse

class PingService:
    def ping(self) -> PingResponse:
        return PingResponse(status="ok", message="MCP server is running")
    
    