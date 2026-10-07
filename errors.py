class GradebookError(Exception):
    """Base exception for all gradebook-related errors."""
    pass

class ValidationError(GradebookError):
    """Raised when data fails validation checks (e.g., bad types, out of bounds)."""
    pass

class NotFoundError(GradebookError):
    """Raised when a requested resource (student, assessment) cannot be found."""
    pass

class ConflictError(GradebookError):
    """Raised when a resource already exists and cannot be duplicated."""
    pass