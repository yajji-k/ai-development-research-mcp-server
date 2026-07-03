from fastmcp import FastMCP

from app.prompts.development.api_documentation_prompt import api_documentation
from app.prompts.development.bug_report_prompt import bug_report
from app.prompts.development.code_review_prompt import code_review

PROMPTS = (
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
)


def register_prompts(server: FastMCP) -> None:
    """Register development prompts with the MCP server."""
    for prompt in PROMPTS:
        server.prompt(
            name=prompt["name"],
            description=prompt["description"],
        )(prompt["handler"])
