from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.utils.response.handlers import ResponseHandler
from app.utils.response.messages import ResponseMessages

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    if errors:
        first_error = errors[0]
        field_name = ".".join([str(loc) for loc in first_error.get("loc", [])])
        msg = first_error.get("msg", "Validation error")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": ResponseMessages.INVALID_DATA_PROVIDED.format(field_name=field_name, msg=msg)
            }
        )
    return ResponseHandler.bad_request(message=ResponseMessages.VALIDATION_ERROR)
