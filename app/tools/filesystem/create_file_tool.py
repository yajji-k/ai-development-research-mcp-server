from app.schemas.filesystem import CreateFileResponse
from app.services.development import FileService
from app.telemetry.decorators import tool_execution

service = FileService()


@tool_execution
def create_file(path: str, content: str = "") -> CreateFileResponse:
    """
    Create a new file within the configured workspace.
    """
    return service.create_file(
        path=path,
        content=content,
    )
