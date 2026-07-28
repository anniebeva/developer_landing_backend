class ContactCreationError(Exception):
    """Raised when contact request cannot be created."""

    def __init__(self, message: str = "Failed to create contact request"):
        self.message = message
        super().__init__(message)
