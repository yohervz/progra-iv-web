"""Domain specific exceptions."""


class DomainException(Exception):
    """Base domain exception."""
    pass


class CourseNotFoundError(DomainException):
    """Raised when a requested course cannot be found."""
    def __init__(self, identifier: str):
        super().__init__(f"No se encontró el curso solicitado con identificador: '{identifier}'.")
        self.identifier = identifier


class InvalidEnrollmentError(DomainException):
    """Raised when an enrollment violates domain validation rules."""
    def __init__(self, message: str, errors: dict | None = None):
        super().__init__(message)
        self.errors = errors or {}
