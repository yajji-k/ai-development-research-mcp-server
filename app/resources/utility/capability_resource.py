from fastmcp.resources import ResourceResult, ResourceContent

from app.telemetry.decorators import resource_execution
from app.services.utility import CapabilitiesService

service = CapabilitiesService()


@resource_execution
def capability()->ResourceResult:
    response = service.get_capability()
    
    return ResourceResult([
        ResourceContent(
            response,
            mime_type="application/json"
        )
    ])
