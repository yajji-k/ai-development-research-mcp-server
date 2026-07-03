import logging
from argparse import ArgumentParser, Namespace

from fastapi import FastAPI
import uvicorn

from app.api.app import create_app
from app.config.settings import Transport, get_settings
from app.server.app import create_server
from app.telemetry.logging_config import configure_logging

logger = logging.getLogger(__name__)


def parse_args() -> Namespace:
    parser = ArgumentParser(description="Run the MCP server.")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Restart the HTTP server when source files change.",
    )

    return parser.parse_args()


def create_http_app() -> FastAPI:
    mcp = create_server()
    return create_app(mcp)


def main() -> None:
    configure_logging()
    args = parse_args()

    try:
        settings = get_settings()

        logger.info("Starting MCP server...")

        mcp = create_server()

        if settings.transport == Transport.STDIO:
            logger.info("Running MCP server using STDIO transport.")
            mcp.run()

        elif settings.transport == Transport.HTTP:
            logger.info(
                "Running MCP server using HTTP transport on %s:%s",
                settings.http_host,
                settings.http_port,
            )

            app = create_app(mcp)

            if args.reload:
                uvicorn.run(
                    "app.server.bootstrap:create_http_app",
                    factory=True,
                    host=settings.http_host,
                    port=settings.http_port,
                    reload=True,
                )
            else:
                uvicorn.run(
                    app,
                    host=settings.http_host,
                    port=settings.http_port,
                )

    except Exception:
        logger.exception("Fatal error while starting MCP server.")
        raise

    finally:
        logger.info("MCP server stopped.")


if __name__ == "__main__":
    main()
