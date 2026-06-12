from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.auth import UserLogin, UserLoginResponse, SetMPinRequest, CheckMPinRequest, VerifyPasswordRequest
from app.models.user import User
from app.utils.response.handlers import ResponseHandler
from app.utils.response.messages import ResponseMessages

router = APIRouter()

@router.post("/login")
def login(request: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or user.hashed_password != request.password:
        return ResponseHandler.bad_request(message=ResponseMessages.INVALID_CREDENTIALS)

    access_token = "fake-access-token"
    refresh_token = "fake-refresh-token"

    return ResponseHandler.success(
        response_data={'access': access_token, 'refresh': refresh_token},
        message=ResponseMessages.LOGIN_SUCCESS
    )


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ResponseHandler.success(message=ResponseMessages.LOGOUT_SUCCESS)

@router.patch("/set-mpin")
def set_mpin(request: SetMPinRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.mpin = request.mpin
    db.commit()
    return ResponseHandler.success(message=ResponseMessages.MPIN_UPDATED)

@router.post("/check-mpin")
def check_mpin(request: CheckMPinRequest, current_user: User = Depends(get_current_user)):
    if current_user.mpin != request.mpin:
        return ResponseHandler.bad_request(message=ResponseMessages.MPIN_INPUT_DOES_NOT_MATCH_SET)
    return ResponseHandler.success(message=ResponseMessages.MPIN_VERIFIED)

@router.post("/verify-password")
def verify_password(request: VerifyPasswordRequest, current_user: User = Depends(get_current_user)):
    if current_user.hashed_password != request.password:
        return ResponseHandler.bad_request(message=ResponseMessages.PASSWORD_MISMATCH)
    return ResponseHandler.success(message=ResponseMessages.PASSWORD_VERIFIED)
