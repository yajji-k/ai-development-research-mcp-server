import logging

import uvicorn

from app.api.app import create_app
from app.config.settings import Transport, get_settings
from app.server.app import create_server
from app.telemetry.logging import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()

    settings = get_settings()

    logger.info("Starting MCP server...")

    mcp = create_server()

    if settings.transport == Transport.STDIO:
        mcp.run()

    elif settings.transport == Transport.HTTP:
        app = create_app(mcp)

        uvicorn.run(
            app,
            host=settings.http_host,
            port=settings.http_port,
        )


if __name__ == "__main__":
    main()