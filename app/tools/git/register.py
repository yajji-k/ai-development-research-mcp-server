from fastmcp import FastMCP

from app.tools.git.git_branch_tool import git_branch
from app.tools.git.git_diff_tool import git_diff
from app.tools.git.git_log_tool import git_log
from app.tools.git.git_status_tool import git_status

TOOLS = (
    git_status,
    git_diff,
    git_log,
    git_branch,
)


def register_tools(server: FastMCP) -> None:
    """Register Git tools with the MCP server."""
    for tool in TOOLS:
        server.tool()(tool)
