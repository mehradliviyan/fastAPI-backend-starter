from collections.abc import Mapping


class AppError(Exception):
    code: str = "application_error"
    message: str = "An application error occurred."

    def __init__(
        self,
        message: str | None = None,
        *,
        details: Mapping[str, object] | None = None,
    ) -> None:
        self.message = message or self.message
        self.details = dict(details or {})

        super().__init__(self.message)