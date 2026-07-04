from app.schemas.filesystem import ReadFileResponse
from app.services.development import FileService
from app.telemetry.decorators import tool_execution

service = FileService()


@tool_execution
def read_file(path: str) -> ReadFileResponse:
    """
    Read a file within the configured workspace.

    Args:
        path: Path of the file to read.

    Returns:
        File contents.
    """
    content = service.read_file(path)

    return ReadFileResponse(
        path=path,
        content=content,
    )
