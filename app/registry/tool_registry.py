from fastmcp import FastMCP

from app.tools.utility import ping, echo, server_info, generate_uuid

utility_tools = [
    ping, echo, server_info, generate_uuid
]

def register_tools(server: FastMCP) -> None:
    """
    Register all MCP tools with the server.
    """
    
    for tool in utility_tools:
        server.tool()(tool)
