from .code_review_prompt import code_review
from .bug_report_prompt import bug_report
from .api_documentation_prompt import api_documentation
from .register import register_prompts

__all__ = [
    "code_review",
    "bug_report",
    "api_documentation",
    "register_prompts",
]
