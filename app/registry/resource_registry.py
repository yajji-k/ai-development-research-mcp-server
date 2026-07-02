from fastmcp import FastMCP

from app.resources.utility import server_info, health, capability

utility_resources = [
    ("server://info", server_info),
    ("server://health", health),
    ("server://capabilities", capability),
]

def register_resources(server: FastMCP) -> None:
    """
    Register all MCP tools with the server.
    """
    
    for uri, resource in utility_resources:
        server.resource(uri)(resource)