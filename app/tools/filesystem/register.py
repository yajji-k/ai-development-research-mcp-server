from fastmcp import FastMCP

from app.tools.filesystem.create_file_tool import create_file
from app.tools.filesystem.delete_file_tool import delete_file
from app.tools.filesystem.edit_file_tool import edit_file
from app.tools.filesystem.list_directory_tool import list_directory
from app.tools.filesystem.read_file_tool import read_file

TOOLS = (
    read_file,
    create_file,
    edit_file,
    delete_file,
    list_directory,
)


def register_tools(server: FastMCP) -> None:
    """Register filesystem tools with the MCP server."""
    for tool in TOOLS:
        server.tool()(tool)
