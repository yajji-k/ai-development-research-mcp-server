from app.schemas.utility import PingResponse
from app.services.utility import PingService

def test_ping_returns_success_response():
    service = PingService()
    
    response = service.ping()
    
    assert isinstance(response, PingResponse)
    assert response.status == "ok"
    assert response.message == "MCP server is running"