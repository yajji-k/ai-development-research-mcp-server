from .base import MCPServerError

class ValidationError(MCPServerError):
    """Raised when user input fails validation."""
    pass