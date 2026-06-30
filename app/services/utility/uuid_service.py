import uuid

from app.schemas.utility import UUIDResponse

class UUIDService:
    """
    Application service for UUID
    """
    
    def get_uuid(self)-> UUIDResponse:
        
        return UUIDResponse(
            uuid=str(uuid.uuid4())
        )