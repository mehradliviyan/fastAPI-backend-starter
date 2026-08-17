from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from backend.presentation.http.errors.schemas import ErrorBody, ErrorResponse
from backend.shared_kernel.exceptions import (
    AppError,
    AuthenticationError,
    BusinessRuleViolationError,
    ConflictError,
    PermissionDeniedError,
    ResourceNotFoundError,
)


from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException as StarletteHTTPException


import logging

logger = logging.getLogger(__name__)

_ERROR_STATUS_CODES: tuple[tuple[type[AppError], int], ...] = (
    (BusinessRuleViolationError, status.HTTP_422_UNPROCESSABLE_CONTENT),
    (ResourceNotFoundError, status.HTTP_404_NOT_FOUND),
    (ConflictError, status.HTTP_409_CONFLICT),
    (AuthenticationError, status.HTTP_401_UNAUTHORIZED),
    (PermissionDeniedError, status.HTTP_403_FORBIDDEN),
)

_HTTP_ERROR_RESPONSES: dict[int, tuple[str, str]] = {
    status.HTTP_404_NOT_FOUND: (
        "route_not_found",
        "The requested endpoint was not found.",
    ),
    status.HTTP_405_METHOD_NOT_ALLOWED: (
        "method_not_allowed",
        "The requested HTTP method is not allowed.",
    ),
}


def _get_status_code(exception: AppError) -> int:
    for error_type, status_code in _ERROR_STATUS_CODES:
        if isinstance(exception, error_type):
            return status_code

    return status.HTTP_400_BAD_REQUEST


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
        status_code=_get_status_code(exception),
        content=response.model_dump(mode="json"),
    )



async def handle_request_validation_error(
    _request: Request,
    exception: RequestValidationError,
) -> JSONResponse:
    response = ErrorResponse(
        error=ErrorBody(
            code="request_validation_error",
            message="Request validation failed.",
            details={
                "errors": jsonable_encoder(exception.errors()),
            },
        )
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=response.model_dump(mode="json"),
    )
    
    
async def handle_http_exception(
    _request: Request,
    exception: StarletteHTTPException,
) -> JSONResponse:
    default_message = (
        exception.detail
        if isinstance(exception.detail, str)
        else "The HTTP request could not be completed."
    )

    code, message = _HTTP_ERROR_RESPONSES.get(
        exception.status_code,
        ("http_error", default_message),
    )

    response = ErrorResponse(
        error=ErrorBody(
            code=code,
            message=message,
        )
    )

    return JSONResponse(
        status_code=exception.status_code,
        content=response.model_dump(mode="json"),
        headers=exception.headers,
    )


async def handle_unexpected_exception(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    logger.error(
        "Unhandled exception while processing %s %s",
        request.method,
        request.url.path,
        extra={
            "method": request.method,
            "path": request.url.path,
        },
        exc_info=(
            type(exception),
            exception,
            exception.__traceback__,
        ),
    )

    response = ErrorResponse(
        error=ErrorBody(
            code="internal_server_error",
            message="An unexpected error occurred.",
        )
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(mode="json"),
    )
    
def register_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(AppError, handle_app_error)
    application.add_exception_handler(
        RequestValidationError,
        handle_request_validation_error,
    )
    application.add_exception_handler(
        StarletteHTTPException,
        handle_http_exception,
    )
    application.add_exception_handler(
        Exception,
        handle_unexpected_exception,
    )