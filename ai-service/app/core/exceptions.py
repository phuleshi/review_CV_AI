"""Domain-level exceptions, mapped to HTTP responses by the error handler."""


class AIServiceError(Exception):
    """Base error for all expected (handled) failures in the service."""

    status_code: int = 500

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


class CVParsingError(AIServiceError):
    status_code = 422


class ReviewError(AIServiceError):
    status_code = 502
