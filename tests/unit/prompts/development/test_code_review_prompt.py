from unittest.mock import Mock

import app.prompts.development.code_review_prompt as code_review_prompt


def test_code_review_prompt_calls_service_and_returns_response_unchanged(monkeypatch):
    language = "Python"
    service = Mock()
    expected_response = object()
    service.get_code_review_prompt.return_value = expected_response
    monkeypatch.setattr(code_review_prompt, "service", service)

    response = code_review_prompt.code_review(language)

    service.get_code_review_prompt.assert_called_once_with(language)
    assert response is expected_response
