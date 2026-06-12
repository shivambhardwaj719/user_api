import jwt
from datetime import datetime, timezone
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY

def get_tokens_for_user(user, db):
    now = datetime.now(timezone.utc)
    user.auth_token_issued_at = now
    db.commit()

    iat_timestamp = int(now.timestamp())
    exp_access = iat_timestamp + 3600
    exp_refresh = iat_timestamp + (86400 * 7)
    sub = f"{user.id}-{'true' if user.is_super_admin else 'false'}"
    
    access_payload = {
        "user_id": user.id,
        "sub": sub,
        "iat": iat_timestamp,
        "exp": exp_access,
        "impersonation": False,
        "type": "access"
    }
    
    refresh_payload = {
        "user_id": user.id,
        "sub": sub,
        "iat": iat_timestamp,
        "exp": exp_refresh,
        "impersonation": False,
        "type": "refresh"
    }
    
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")
    
    return {
        'access': access_token,
        'refresh': refresh_token
    }

def generate_impersonation_tokens(user, db):
    issued_at = user.auth_token_issued_at or datetime.now(timezone.utc)
    iat_timestamp = int(issued_at.timestamp())
    exp_access = iat_timestamp + 3600
    exp_refresh = iat_timestamp + (86400 * 7)

    sub = f"{user.id}-true"
    
    access_payload = {
        "user_id": user.id,
        "sub": sub,
        "iat": iat_timestamp,
        "exp": exp_access,
        "impersonation": True,
        "type": "access"
    }
    
    refresh_payload = {
        "user_id": user.id,
        "sub": sub,
        "iat": iat_timestamp,
        "exp": exp_refresh,
        "impersonation": True,
        "type": "refresh"
    }
    
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")
    
    return {
        'access': access_token,
        'refresh': refresh_token
    }
