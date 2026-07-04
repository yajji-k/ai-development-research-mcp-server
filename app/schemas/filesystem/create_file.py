from pydantic import BaseModel


class CreateFileResponse(BaseModel):
    path: str
    message: str
