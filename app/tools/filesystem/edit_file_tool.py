from app.schemas.filesystem import EditFileResponse
from app.services.development import FileService
from app.telemetry.decorators import tool_execution


service = FileService()


@tool_execution
def edit_file(path: str, content: str) -> EditFileResponse:
    """
    Replace the contents of an existing file.

    Args:
        path: Path of the file to edit.
        content: New file contents.

    Returns:
        Information about the edited file.
    """
    service.edit_file(
        path=path,
        content=content,
    )

    return EditFileResponse(
        path=path,
        message="File updated successfully.",
    )
