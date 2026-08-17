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
        
class BusinessRuleViolationError(AppError):
    code = "business_rule_violation"
    message = "A business rule was violated."


class ResourceNotFoundError(AppError):
    code = "resource_not_found"
    message = "The requested resource was not found."


class ConflictError(AppError):
    code = "conflict"
    message = "The requested operation conflicts with the current state."


class AuthenticationError(AppError):
    code = "authentication_error"
    message = "Authentication failed."


class PermissionDeniedError(AppError):
    code = "permission_denied"
    message = "You do not have permission to perform this operation."