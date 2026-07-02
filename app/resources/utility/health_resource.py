from fastmcp.resources import ResourceResult, ResourceContent

from app.telemetry.decorators import resource_execution
from app.services.utility import HealthService

service = HealthService()

@resource_execution
def health() -> ResourceResult:
    response = service.get_health()
    
    return ResourceResult([
        ResourceContent(
            response,
            mime_type="application/json"
        )
    ])
