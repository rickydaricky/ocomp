class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class UserNotInDatabaseError(Error):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message