from fastapi.testclient import TestClient

from backend.bootstrap.application import create_app
from backend.config.settings import AppEnvironment, Settings
from backend.shared_kernel.exceptions import AppError


class SampleBusinessError(AppError):
    code = "sample_business_error"
    message = "A sample business rule failed."


def test_app_error_is_converted_to_standard_http_response() -> None:
    settings = Settings(
        _env_file=None,
        name="Backend Starter Test",
        version="0.1.0",
        environment=AppEnvironment.TEST,
        debug=False,
    )
    application = create_app(settings)

    @application.get("/test-error")
    async def raise_sample_error() -> None:
        raise SampleBusinessError(details={"field": "sample"})

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