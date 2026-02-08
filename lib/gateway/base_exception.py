from typing import Optional


class CustomException(Exception):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or self.__class__.__name__)


class GatewayConnectionError(CustomException):
    pass


class GatewayError(CustomException):
    def __init__(self, code: int, text: Optional[str] = None, message: Optional[str] = None):
        self.code = code
        self.text = text
        full_message = message or f"GatewayError {code}: {text}"
        super().__init__(full_message)
