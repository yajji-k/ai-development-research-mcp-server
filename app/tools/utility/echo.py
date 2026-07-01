from app.telemetry.decorators import tool_execution
from app.services.utility import EchoService

service = EchoService()

@tool_execution
def get_echo(message:str):
    """Mcp tool adapter for echo"""
    return service.echo(message=message)