from pydantic import BaseModel


class DeleteFileResponse(BaseModel):
    path: str
    message: str
