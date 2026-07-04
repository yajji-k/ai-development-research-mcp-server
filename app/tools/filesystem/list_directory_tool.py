from app.schemas.filesystem import ListDirectoryResponse
from app.services.development import FileService
from app.telemetry.decorators import tool_execution


service = FileService()


@tool_execution
def list_directory(path: str = ".") -> ListDirectoryResponse:
    """
    List the contents of a directory.

    Args:
        path: Directory path relative to the workspace.

    Returns:
        Directory contents.
    """
    return service.list_directory(path)
