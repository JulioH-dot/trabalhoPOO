from src.enums.enum import ErrorType

class CustomException(Exception):
    def __init__(self, error_type: ErrorType, message: str):
      self.error_type = error_type
      self.message = message
      super().__init__(message)

    def http_status_code(self):
      return self.error_type.http_status_code()