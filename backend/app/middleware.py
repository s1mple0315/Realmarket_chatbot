from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.services.auth_service import verify_token

class AddUserIDToRequest(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Assuming the token is passed in the headers for extracting user ID
        token = request.headers.get("Authorization")
        
        if token is None:
            request.state.user_id = None  # Or raise an exception if needed
        else:
            # Extract the user_id from the token, for example using JWT decoding
            # Assuming you have a function `decode_token` for JWT validation and decoding
            try:
                payload = verify_token(token)
                request.state.user_id = payload.get("sub")  # Extract user ID from the token
            except Exception as e:
                request.state.user_id = None  # Or handle the exception based on your logic
        
        response = await call_next(request)
        return response
