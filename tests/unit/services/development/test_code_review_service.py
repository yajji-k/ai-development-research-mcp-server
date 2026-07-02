import pytest

from app.services.development import CodeReviewService


@pytest.fixture
def language() -> str:
    return "Python"


def test_code_review_prompt_returns_string(language):
    service = CodeReviewService()

    prompt = service.get_code_review_prompt(language)

    assert isinstance(prompt, str)


def test_code_review_prompt_contains_language(language):
    service = CodeReviewService()

    prompt = service.get_code_review_prompt(language)

    assert language in prompt


def test_code_review_prompt_contains_important_sections(language):
    service = CodeReviewService()

    prompt = service.get_code_review_prompt(language)

    for section in ("Correctness", "Readability", "Security", "Performance"):
        assert section in prompt
