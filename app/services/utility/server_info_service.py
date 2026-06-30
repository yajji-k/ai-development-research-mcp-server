import platform

from app.config.settings import get_settings
from app.schemas.utility.server_info import ServerInfoResponse

class ServerInfoService:
    """Application service for server information."""

    def get_server_info(self) -> ServerInfoResponse:
        settings = get_settings()
        
        return ServerInfoResponse(
            server_name=settings.server_name,
            server_version=settings.server_version,
            python_version=platform.python_version(),
            log_level=settings.log_level,
            transport="stdio"
        )