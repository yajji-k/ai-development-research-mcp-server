from pydantic import BaseModel

class ServerInfoResponse(BaseModel):
    """
    Response returned by the server info tool.
    """

    server_name: str
    server_version: str
    python_version: str
    log_level: str
    transport: str