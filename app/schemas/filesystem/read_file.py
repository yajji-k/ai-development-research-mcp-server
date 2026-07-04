from pydantic import BaseModel


class ReadFileResponse(BaseModel):
    path: str
    content: str
