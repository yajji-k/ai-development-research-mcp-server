from app.services.development import CodeReviewService
from app.telemetry.decorators import prompt_execution

service = CodeReviewService()

@prompt_execution
def code_review(language: str):
    return service.get_code_review_prompt(language)