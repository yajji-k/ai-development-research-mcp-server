from unittest.mock import Mock

import app.prompts.development.api_documentation_prompt as api_documentation_prompt


def test_api_documentation_prompt_calls_service_and_returns_response_unchanged(monkeypatch):
    framework = "FastAPI"
    service = Mock()
    expected_response = object()
    service.get_api_doc_prompt.return_value = expected_response
    monkeypatch.setattr(api_documentation_prompt, "service", service)

    response = api_documentation_prompt.api_documentation(framework)

    service.get_api_doc_prompt.assert_called_once_with(framework=framework)
    assert response is expected_response
