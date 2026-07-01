from fastmcp import FastMCP

from app.tools.utility import ping, echo, uuid

utility_tools = [
    ping, 
    echo, 
    uuid
]

def register_tools(server: FastMCP) -> None:
    """
    Register all MCP tools with the server.
    """
    
    for tool in utility_tools:
        server.tool()(tool)
