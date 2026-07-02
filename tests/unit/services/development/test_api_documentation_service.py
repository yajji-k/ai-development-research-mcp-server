import pytest

from app.services.development import APIDocumentationService


@pytest.fixture
def framework() -> str:
    return "FastAPI"


def test_api_documentation_prompt_returns_string(framework):
    service = APIDocumentationService()

    prompt = service.get_api_doc_prompt(framework)

    assert isinstance(prompt, str)


def test_api_documentation_prompt_contains_framework(framework):
    service = APIDocumentationService()

    prompt = service.get_api_doc_prompt(framework)

    assert framework in prompt


def test_api_documentation_prompt_contains_important_sections(framework):
    service = APIDocumentationService()

    prompt = service.get_api_doc_prompt(framework)

    for section in ("HTTP Method", "Response Body", "Request Body", "Error Responses"):
        assert section in prompt
