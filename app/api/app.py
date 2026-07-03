from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from app.auth.api_key import APIKeyMiddleware
from fastmcp import FastMCP


def create_app(mcp: FastMCP) -> FastAPI:
    """
    Create and configure the FastAPI application.

    Additional configuration such as middleware, routes,
    health checks, authentication, and the MCP server
    will be added incrementally.
    """

    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Development only
            allow_credentials=True,
            allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
            allow_headers=[
                "Content-Type",
                "Authorization",
                "mcp-session-id",
                "mcp-protocol-version",
            ],
            expose_headers=[
                "mcp-session-id",
            ],
        ),
        Middleware(APIKeyMiddleware)
    ]

    mcp_app = mcp.http_app(
        path="/mcp",
        middleware=middleware,
    )

    app = FastAPI(
        title="Production-Grade MCP Server",
        description="HTTP host application for the MCP Server.",
        version="1.0.0",
        lifespan=mcp_app.lifespan,
    )

    app.mount("/mcp-server",mcp_app)

    return app