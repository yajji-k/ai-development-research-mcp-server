from app.services.development import BugReportService
from app.telemetry.decorators import prompt_execution
service = BugReportService()

@prompt_execution
def bug_report(project_name:str):
    response = service.build_bug_report_prompt(project_name=project_name)
    return response
