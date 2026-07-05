from app.schemas.git import GitDiffResponse
from app.services.git import GitService
from app.telemetry.decorators import tool_execution

service = GitService()


@tool_execution
def git_diff(staged: bool = False) -> GitDiffResponse:
    """
    Show Git diff for the configured workspace.
    """
    return service.git_diff(staged=staged)
