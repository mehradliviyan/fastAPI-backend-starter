from backend.bootstrap.application import create_app
from backend.config.settings import AppEnvironment, Settings


def test_create_app_uses_provided_settings() -> None:
    settings = Settings(
        _env_file=None,
        name="Test Application",
        version="9.9.9",
        environment=AppEnvironment.TEST,
        debug=True,
    )

    application = create_app(settings)

    assert application.title == "Test Application"
    assert application.version == "9.9.9"
    assert application.debug is True