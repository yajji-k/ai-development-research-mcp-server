from pydantic import BaseModel

class EchoResponse(BaseModel):
    """
    Response returned by the echo service
    """
    message: str