import uuid
import hashlib
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class ClientIdentificationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.cookie_name = 'user_id'
        self.cookie_max_age = 30 * 24 * 60 * 60 # 30 days
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        if not request.cookies.get(self.cookie_name):
            client_id = self.generate_client_id(request)
            response.set_cookie(
                key=self.cookie_name,
                value=client_id,
                max_age=self.cookie_max_age,
                httponly=True,
                secure=True,
                samesite='lax'
            )
        
        return response
    
    def generate_client_id(self, request: Request):
        user_agent = request.headers.get('User-Agent', '')
        unique_data = f"{uuid.uuid4()}-{user_agent}"
        return hashlib.sha256(unique_data.encode()).hexdigest()[:32]
