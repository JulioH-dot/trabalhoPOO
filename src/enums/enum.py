from enum import Enum

class ErrorType(Enum):
    INVALID_EMAIL = "Invalid email format"
    NOT_FOUND = "Not Found Exception"
    DATABASE_ERROR = "Database error"
    INVALID_CREDENTIALS = "Credentials invalid"
    INVALID_OPERATION = "Invalid operation"

    def http_status_code(self):
        # Mapeamento entre o tipo de erro e o código HTTP correspondente
        status_codes = {
            ErrorType.INVALID_EMAIL: 400,  # Bad Request
            ErrorType.NOT_FOUND: 404,  # Not Found
            ErrorType.DATABASE_ERROR: 500,  # Internal Server Error
            ErrorType.INVALID_CREDENTIALS: 401,  # Unauthorized
            ErrorType.INVALID_OPERATION: 400  # Bad Request
        }
        return status_codes.get(self, 500)
