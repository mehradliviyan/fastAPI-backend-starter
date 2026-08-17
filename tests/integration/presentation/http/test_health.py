from fastapi.testclient import TestClient

from backend.bootstrap.application import create_app
from backend.config.settings import AppEnvironment, Settings


def test_health_endpoint_returns_ok() -> None:
    test_settings = Settings(
        _env_file=None,
        name="Backend Starter Test",
        version="0.1.0",
        environment=AppEnvironment.TEST,
        debug=False,
    )

    with TestClient(create_app(test_settings)) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}