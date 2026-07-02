from fastmcp import FastMCP

from app.prompts.development import code_review

development_prompts = [
    {
        "handler": code_review,
        "name": "code_review",
        "description": "Generate a prompt for reviewing source code.",
    },
]

def register_prompts(server: FastMCP) -> None:
    """
    Register all MCP tools with the server.
    """
    
    for prompt in development_prompts:
        server.prompt(name=prompt["name"], description=prompt["description"])(prompt["handler"])