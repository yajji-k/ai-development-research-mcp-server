from app.schemas.utility.echo import EchoResponse

class EchoService:
    """
    Application service for echo operations
    """
    def echo(self, message: str) -> EchoResponse:
        return EchoResponse(message=message)