from fastmcp import FastMCP

from app.tools.utility import get_ping, get_echo, get_server_info, get_uuid

utility_tools = [
    get_ping, 
    get_echo, 
    get_server_info, 
    get_uuid
]

def register_tools(server: FastMCP) -> None:
    """
    Register all MCP tools with the server.
    """
    
    for tool in utility_tools:
        server.tool()(tool)
