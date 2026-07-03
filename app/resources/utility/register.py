from fastmcp import FastMCP

from app.resources.utility.capability_resource import capability
from app.resources.utility.health_resource import health
from app.resources.utility.server_info_resource import server_info

RESOURCES = (
    ("server://info", server_info),
    ("server://health", health),
    ("server://capabilities", capability),
)


def register_resources(server: FastMCP) -> None:
    """Register utility resources with the MCP server."""
    for uri, resource in RESOURCES:
        server.resource(uri)(resource)
