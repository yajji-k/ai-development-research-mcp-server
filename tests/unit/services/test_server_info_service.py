import platform

from app.config.settings import get_settings
from app.schemas.utility import ServerInfoResponse
from app.services.utility import ServerInfoService


def test_server_info_returns_application_information() -> None:
    service = ServerInfoService()
    settings = get_settings()

    response = service.get_server_info()

    assert isinstance(response, ServerInfoResponse)
    assert response.server_name == settings.server_name
    assert response.server_version == settings.server_version
    assert response.log_level == settings.log_level
    assert response.transport == "stdio"
    assert response.python_version == platform.python_version()