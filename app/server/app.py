from fastmcp import FastMCP

from app.config.settings import get_settings
from app.tools.tool_registry import register_tools


def create_server() -> FastMCP:
    """
    Create and configure the FastMCP server instance.
    """
    settings = get_settings()

    server = FastMCP(
        name=settings.server_name,
    )

    register_tools(server)

    return server
