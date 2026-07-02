import pytest

from app.exceptions import ValidationError
from app.schemas.utility import EchoResponse
from app.services.utility import EchoService


def test_echo_returns_same_message():
    service = EchoService()

    response = service.echo("Hello MCP")

    assert isinstance(response, EchoResponse)
    assert response.message == "Hello MCP"


def test_echo_validation_error_for_empty_message():
    service = EchoService()

    with pytest.raises(ValidationError, match="Message Cannot be empty"):
        service.echo("")


def test_echo_validation_error_for_whitespace_message():
    service = EchoService()

    with pytest.raises(ValidationError, match="Message Cannot be empty"):
        service.echo("     ")
