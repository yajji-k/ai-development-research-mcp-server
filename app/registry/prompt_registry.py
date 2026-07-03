from app.prompts import development
from fastmcp import FastMCP

PROMPT_REGISTRARS = (
    development.register_prompts,
)


def register_prompts(server: FastMCP) -> None:
    """Register all MCP prompts with the server."""
    for register in PROMPT_REGISTRARS:
        register(server)
