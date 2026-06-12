import jwt
import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.models.user import User
from app.utils.response.handlers import ResponseHandler
from app.utils.response.messages import ResponseMessages
from app.api.deps import SessionLocal
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY

class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    ALLOWED_PATHS_FOR_NO_AUTH = [
        '/api/v1/auth/login',
        '/docs',
        '/openapi.json',
        '/redoc',
        '/api/v1/auth/verify-password',
        '/api/v1/auth/check-mpin'
    ]

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(p) for p in self.ALLOWED_PATHS_FOR_NO_AUTH):
            return await call_next(request)

        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return ResponseHandler.unauthorized(message=ResponseMessages.AUTH_HEADER_MISSING_OR_INVALID)

        token = auth_header.split(' ')[1]

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return ResponseHandler.unauthorized(message=ResponseMessages.TOKEN_EXPIRED)
        except jwt.InvalidTokenError:
            return ResponseHandler.unauthorized(message=ResponseMessages.INVALID_TOKEN)

        sub = decoded.get('sub', '')
        try:
            user_id, impersonation_flag = sub.split('-')
            user_id = int(user_id)
            impersonation_flag = impersonation_flag.lower()
        except ValueError:
            return ResponseHandler.unauthorized(message=ResponseMessages.INVALID_TOKEN_SUBJECT)

        db = SessionLocal()
        try:
            user = db.query(User).filter(
                User.id == user_id
            ).first()

            if not user:
                return ResponseHandler.unauthorized(message=ResponseMessages.USER_NOT_FOUND)

            token_iat = decoded.get('iat')
            if token_iat is None:
                return ResponseHandler.unauthorized(message=ResponseMessages.TOKEN_MISSING_IAT)

            request.state.user = user
            request.state.is_superuser_or_impersonation = (
                user.is_super_admin or impersonation_flag == 'true' or user.account_type == 'super_admin'
            )
            
        finally:
            db.close()

        response = await call_next(request)
        return response
