from fastmcp.server.lifespan import lifespan


@lifespan
async def app_lifespan(server):
    """
    Manage application startup and shutdown.
    """

    # Startup
    yield {}

    # Shutdown
