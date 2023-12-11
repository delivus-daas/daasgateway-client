class DaaSGatewayError(Exception):
    """Base class for exceptions in this module."""
    pass


class DaaSGatewayClientError(DaaSGatewayError):
    """Exception raised for errors in the DaaSGatewayClient class."""

    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
