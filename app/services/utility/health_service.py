from app.schemas.utility import HealthResponse

class HealthService:
    def get_health(self) -> HealthResponse:
        return HealthResponse(status="healthy")