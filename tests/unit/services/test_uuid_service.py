import uuid

from app.schemas.utility import UUIDResponse
from app.services.utility import UUIDService


def test_generate_uuid_response_success():
    service = UUIDService()
    
    response = service.get_uuid()
    
    assert isinstance(response, UUIDResponse)
    
    parsed_uuid = uuid.UUID(response.uuid)

    assert str(parsed_uuid) == response.uuid