import pytest

from app.services.development import BugReportService


@pytest.fixture
def project_name() -> str:
    return "MCP Server"


def test_bug_report_prompt_returns_string(project_name):
    service = BugReportService()

    prompt = service.build_bug_report_prompt(project_name)

    assert isinstance(prompt, str)


def test_bug_report_prompt_contains_project_name(project_name):
    service = BugReportService()

    prompt = service.build_bug_report_prompt(project_name)

    assert project_name in prompt


def test_bug_report_prompt_contains_important_sections(project_name):
    service = BugReportService()

    prompt = service.build_bug_report_prompt(project_name)

    for section in ("Steps to Reproduce", "Severity", "Expected Behavior", "Actual Behavior"):
        assert section in prompt
