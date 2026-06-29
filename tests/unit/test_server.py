from fastmcp import FastMCP

from app.server.app import create_server


def test_create_server_returns_fastmcp_instance() -> None:
    server = create_server()

    assert isinstance(server, FastMCP)