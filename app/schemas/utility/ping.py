from pydantic import BaseModel

class PingResponse(BaseModel):
    """
    Response returned by the ping service.
    """
    status:str
    message:str