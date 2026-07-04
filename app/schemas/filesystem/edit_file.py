from pydantic import BaseModel


class EditFileResponse(BaseModel):
    path: str
    message: str
