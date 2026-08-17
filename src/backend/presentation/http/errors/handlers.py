from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from backend.presentation.http.errors.schemas import ErrorBody, ErrorResponse
from backend.shared_kernel.exceptions import AppError


async def handle_app_error(
    _request: Request,
    exception: AppError,
) -> JSONResponse:
    response = ErrorResponse(
        error=ErrorBody(
            code=exception.code,
            message=exception.message,
            details=exception.details,
        )
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=response.model_dump(mode="json"),
    )


def register_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(AppError, handle_app_error)