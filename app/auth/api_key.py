from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config.settings import get_settings

class APIKeyMiddleware(BaseHTTPMiddleware):
    """Authenticate HTTP requests using an API key."""
    async def dispatch(self, request:Request, call_next: RequestResponseEndpoint) -> Response:
        settings = get_settings()
        
        authorization = request.headers.get('Authorization')
        
        if authorization is None:
            return self.invalid_auth_response()
            
        if not authorization.startswith('Bearer '):
            return self.invalid_auth_response()
        
        api_key = authorization.removeprefix("Bearer ")

        if api_key != settings.api_key:
            return self.invalid_auth_response()      
        

        return await call_next(request)          
    
    def invalid_auth_response(self) -> JSONResponse:
        return JSONResponse(
                status_code=401,
                content={"detail": "Invalid Authorization header"},
            )
            