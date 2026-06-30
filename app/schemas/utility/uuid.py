from pydantic import BaseModel

class UUIDResponse(BaseModel):
    """Response returned by UUID tool"""
    
    uuid:str
