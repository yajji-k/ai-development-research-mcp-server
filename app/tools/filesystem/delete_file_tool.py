from app.schemas.filesystem import DeleteFileResponse
from app.services.development import FileService
from app.telemetry.decorators import tool_execution


service = FileService()


@tool_execution
def delete_file(path: str) -> DeleteFileResponse:
    """
    Delete a file within the configured workspace.

    Args:
        path: Path of the file to delete.

    Returns:
        Information about the deleted file.
    """
    return service.delete_file(path)
