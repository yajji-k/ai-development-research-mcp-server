from fastmcp import FastMCP

from app.config.settings import get_settings
from app.registry import register_tools, register_resources, register_prompts

def create_server() -> FastMCP:
    """
    Create and configure the FastMCP server instance.
    """
    settings = get_settings()

    server = FastMCP(
        name=settings.server_name,
    )

    register_tools(server)
    register_resources(server)
    register_prompts(server)
    
    return server
