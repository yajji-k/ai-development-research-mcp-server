from .resource_registry import register_resources
from .tool_registry import register_tools
from .prompt_registry import register_prompts

__all__ = [
    "register_resources",
    "register_tools",
    "register_prompts"
]