from app.schemas.git import GitBranchResponse
from app.services.git import GitService
from app.telemetry.decorators import tool_execution

service = GitService()


@tool_execution
def git_branch() -> GitBranchResponse:
    """
    Show local Git branches for the configured workspace.
    """
    return service.git_branch()
