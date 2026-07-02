from app.services.development import CodeReviewService
from app.telemetry.decorators import prompt_execution

service = CodeReviewService()

@prompt_execution
def code_review(language: str):
    response = service.get_code_review_prompt(language)
    return response