from pydantic import BaseModel


class DirectoryEntry(BaseModel):
    name: str
    is_file: bool
    is_directory: bool
    size: int | None = None


class ListDirectoryResponse(BaseModel):
    path: str
    entries: list[DirectoryEntry]
