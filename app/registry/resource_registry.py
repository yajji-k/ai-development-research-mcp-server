from fastmcp import FastMCP

from app.resources import utility

RESOURCE_REGISTRARS = (
    utility.register_resources,
)


def register_resources(server: FastMCP) -> None:
    """Register all MCP resources with the server."""
    for register in RESOURCE_REGISTRARS:
        register(server)
