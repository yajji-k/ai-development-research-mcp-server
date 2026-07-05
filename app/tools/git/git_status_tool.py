from app.schemas.git import GitStatusResponse
from app.services.git import GitService
from app.telemetry.decorators import tool_execution

service = GitService()


@tool_execution
def git_status() -> GitStatusResponse:
    """
    Show Git status for the configured workspace.
    """
    return service.git_status()
