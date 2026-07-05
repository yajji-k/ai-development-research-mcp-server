import app.tools.filesystem.register
import app.tools.git.register
import app.tools.utility.register
from fastmcp import FastMCP

TOOL_REGISTRARS = (
    app.tools.utility.register.register_tools,
    app.tools.filesystem.register.register_tools,
    app.tools.git.register.register_tools,
)


def register_tools(server: FastMCP) -> None:
    """Register all MCP tools with the server."""
    for register in TOOL_REGISTRARS:
        register(server)
