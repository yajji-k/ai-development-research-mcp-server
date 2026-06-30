from app.services.utility.echo_service import EchoService

service = EchoService()

def echo(message:str):
    """Mcp tool adapter for echo"""
    return service.echo(message=message)