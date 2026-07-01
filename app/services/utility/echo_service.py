from app.exceptions import ValidationError
from app.schemas.utility.echo import EchoResponse

class EchoService:
    """
    Application service for echo operations
    """
    def echo(self, message: str) -> EchoResponse:
        if not message.strip():
            raise ValidationError("Message Cannot be empty")
        
        return EchoResponse(message=message)