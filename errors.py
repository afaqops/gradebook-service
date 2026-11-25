class GradebookError(Exception):
    """Base exception for all gradebook-related errors."""

class ValidationError(GradebookError):
    """Raised when data fails validation checks (e.g., bad types, out of bounds)."""

class NotFoundError(GradebookError):
    """Raised when a requested resource (student, assessment) cannot be found."""

class ConflictError(GradebookError):
    """Raised when a resource already exists and cannot be duplicated."""
