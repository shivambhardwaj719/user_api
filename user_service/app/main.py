from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.api.v1 import auth, staff, user
from app.models.base import Base
from app.api.deps import engine
from app.core.scheduler import start_scheduler
from app.middleware.jwt_auth import JWTAuthenticationMiddleware
from app.middleware.logging import APILoggerMiddleware
from app.middleware.rate_limit import GlobalRateLimitMiddleware
from app.middleware.client_id import ClientIdentificationMiddleware
from app.middleware.exceptions import validation_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Service API",
    description="FastAPI conversion of the okcare user_service.",
    version="1.0.0",
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.on_event("startup")
def on_startup():
    start_scheduler()

app.add_middleware(JWTAuthenticationMiddleware)
app.add_middleware(GlobalRateLimitMiddleware)
app.add_middleware(ClientIdentificationMiddleware)
app.add_middleware(APILoggerMiddleware)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(staff.router, prefix="/api/v1/staff", tags=["Staff"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to User Service FastAPI"}
