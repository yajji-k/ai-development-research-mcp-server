from fastmcp import FastMCP

from app.tools.utility.echo_tool import echo
from app.tools.utility.ping_tool import ping
from app.tools.utility.uuid_tool import uuid

TOOLS = (
    ping,
    echo,
    uuid,
)


def register_tools(server: FastMCP) -> None:
    """Register utility tools with the MCP server."""
    for tool in TOOLS:
        server.tool()(tool)
