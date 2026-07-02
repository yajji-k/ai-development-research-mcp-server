from app.services.development import APIDocumentationService
from app.telemetry.decorators import prompt_execution

service = APIDocumentationService()

@prompt_execution
def api_documentation(framework:str):
    response = service.get_api_doc_prompt(framework=framework)
    return response