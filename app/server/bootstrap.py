from app.server.app import create_server

from app.telemetry.logging import configure_logging

import logging

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()

    logger.info("Starting MCP server...")

    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
