import re
from src.enums.enum import ErrorType
from src.exceptions.custom_exception import CustomException

    
def validate_email(email):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise CustomException(ErrorType.INVALID_EMAIL, "Email não está correto")
