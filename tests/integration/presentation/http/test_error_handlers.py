import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.bootstrap.application import create_app
from backend.config.settings import AppEnvironment, Settings
from backend.shared_kernel.exceptions import (
    AppError,
    AuthenticationError,
    BusinessRuleViolationError,
    ConflictError,
    PermissionDeniedError,
    ResourceNotFoundError,
)


class SampleBusinessError(AppError):
    code = "sample_business_error"
    message = "A sample business rule failed."


def create_error_test_app(exception: AppError) -> FastAPI:
    settings = Settings(
        _env_file=None,
        name="Backend Starter Test",
        version="0.1.0",
        environment=AppEnvironment.TEST,
        debug=False,
    )
    application = create_app(settings)

    @application.get("/test-error")
    async def raise_test_error() -> None:
        raise exception

    return application


def test_plain_app_error_returns_bad_request() -> None:
    exception = SampleBusinessError(details={"field": "sample"})
    application = create_error_test_app(exception)

    with TestClient(application) as client:
        response = client.get("/test-error")

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "sample_business_error",
            "message": "A sample business rule failed.",
            "details": {"field": "sample"},
        }
    }


@pytest.mark.parametrize(
    ("exception", "expected_status_code"),
    [
        (BusinessRuleViolationError(), 422),
        (ResourceNotFoundError(), 404),
        (ConflictError(), 409),
        (AuthenticationError(), 401),
        (PermissionDeniedError(), 403),
    ],
)
def test_semantic_error_category_returns_correct_status_code(
    exception: AppError,
    expected_status_code: int,
) -> None:
    application = create_error_test_app(exception)

    with TestClient(application) as client:
        response = client.get("/test-error")

    assert response.status_code == expected_status_code
    assert response.json()["error"]["code"] == exception.code
    
def test_request_validation_error_uses_standard_response_contract() -> None:
    settings = Settings(
        _env_file=None,
        name="Backend Starter Test",
        version="0.1.0",
        environment=AppEnvironment.TEST,
        debug=False,
    )
    application = create_app(settings)

    @application.get("/test-validation")
    async def validate_limit(limit: int) -> dict[str, int]:
        return {"limit": limit}

    with TestClient(application) as client:
        response = client.get("/test-validation", params={"limit": "invalid"})

    payload = response.json()

    assert response.status_code == 422
    assert payload["error"]["code"] == "request_validation_error"
    assert payload["error"]["message"] == "Request validation failed."
    assert payload["error"]["details"]["errors"][0]["loc"] == [
        "query",
        "limit",
    ]
    
@pytest.mark.parametrize(
    ("method", "path", "expected_status_code", "expected_error_code"),
    [
        ("GET", "/unknown-endpoint", 404, "route_not_found"),
        ("POST", "/health", 405, "method_not_allowed"),
    ],
)
def test_http_exception_uses_standard_response_contract(
    method: str,
    path: str,
    expected_status_code: int,
    expected_error_code: str,
) -> None:
    settings = Settings(
        _env_file=None,
        name="Backend Starter Test",
        version="0.1.0",
        environment=AppEnvironment.TEST,
        debug=False,
    )
    application = create_app(settings)

    with TestClient(application) as client:
        response = client.request(method, path)

    assert response.status_code == expected_status_code
    assert response.json()["error"]["code"] == expected_error_code
    assert response.json()["error"]["details"] == {}
    
def test_unexpected_exception_returns_safe_internal_server_error() -> None:
    settings = Settings(
        _env_file=None,
        name="Backend Starter Test",
        version="0.1.0",
        environment=AppEnvironment.TEST,
        debug=False,
    )
    application = create_app(settings)

    @application.get("/test-unexpected-error")
    async def raise_unexpected_error() -> None:
        raise RuntimeError("sensitive internal information")

    with TestClient(
        application,
        raise_server_exceptions=False,
    ) as client:
        response = client.get("/test-unexpected-error")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "internal_server_error",
            "message": "An unexpected error occurred.",
            "details": {},
        }
    }
    assert "sensitive internal information" not in response.text