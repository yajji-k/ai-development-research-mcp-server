from app.exceptions import ApplicationError
from app.schemas.git import GitLogResponse
from app.services.git import GitService
from app.telemetry.decorators import tool_execution

service = GitService()


@tool_execution
def git_log(limit: int = 10) -> GitLogResponse:
    """
    Show recent Git commits for the configured workspace.
    """
    if limit < 1:
        raise ApplicationError("Git log limit must be greater than 0")

    return service.git_log(limit=limit)
