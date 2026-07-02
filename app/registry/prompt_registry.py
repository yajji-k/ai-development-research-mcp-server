from fastmcp import FastMCP

from app.prompts.development import code_review, bug_report, api_documentation

development_prompts = [
    {
        "handler": code_review,
        "name": "code_review",
        "description": "Generate a prompt for reviewing source code.",
    },
    {
        "handler": bug_report,
        "name": "bug_report",
        "description": "Generate a prompt for creating bug reports.",
    },
    {
        "handler": api_documentation,
        "name": "api_documentation",
        "description": "Generate a prompt for creating API documentation.",    
    },
]

def register_prompts(server: FastMCP) -> None:
    """
    Register all MCP prompts with the server.
    """
    
    for prompt in development_prompts:
        server.prompt(name=prompt["name"], description=prompt["description"])(prompt["handler"])
