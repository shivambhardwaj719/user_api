from fastapi.responses import JSONResponse
from fastapi import status
from .messages import ResponseMessages

class ResponseHandler:
    @staticmethod
    def success(response_data=None, message=ResponseMessages.SUCCESS):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"success": True, "message": message, "data": response_data}
        )

    @staticmethod
    def create_success(name="Resource"):
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"success": True, "message": ResponseMessages.create_success_message(name)}
        )

    @staticmethod
    def update_success(name="Resource"):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"success": True, "message": ResponseMessages.update_success_message(name)}
        )

    @staticmethod
    def delete_success(name="Resource"):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"success": True, "message": f"{name} deleted successfully"}
        )

    @staticmethod
    def bad_request(response_data=None, message=ResponseMessages.BAD_REQUEST):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "message": message, "errors": response_data}
        )

    @staticmethod
    def unauthorized(message=ResponseMessages.UNAUTHORIZED):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"success": False, "message": message}
        )

    @staticmethod
    def forbidden(message=ResponseMessages.FORBIDDEN):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"success": False, "message": message}
        )

    @staticmethod
    def not_found(message=ResponseMessages.NOT_FOUND):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"success": False, "message": message}
        )

    @staticmethod
    def no_matching_data(message=ResponseMessages.NO_MATCHING_DATA):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"success": False, "message": message}
        )

    @staticmethod
    def list_success(data):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"success": True, "data": data}
        )

    @staticmethod
    def create_failed(errors=None, message=ResponseMessages.CREATE_FAILED):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "message": message, "errors": errors}
        )

    @staticmethod
    def update_failed(errors=None, message=ResponseMessages.UPDATE_FAILED):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "message": message, "errors": errors}
        )

    @staticmethod
    def dependency_error(message=ResponseMessages.DELETE_ERROR):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "message": message}
        )
