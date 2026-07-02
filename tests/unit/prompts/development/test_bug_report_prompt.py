from unittest.mock import Mock

import app.prompts.development.bug_report_prompt as bug_report_prompt


def test_bug_report_prompt_calls_service_and_returns_response_unchanged(monkeypatch):
    project_name = "MCP Server"
    service = Mock()
    expected_response = object()
    service.build_bug_report_prompt.return_value = expected_response
    monkeypatch.setattr(bug_report_prompt, "service", service)

    response = bug_report_prompt.bug_report(project_name)

    service.build_bug_report_prompt.assert_called_once_with(project_name=project_name)
    assert response is expected_response
