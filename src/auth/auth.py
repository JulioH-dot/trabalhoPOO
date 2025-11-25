from flask_jwt_extended import create_access_token, create_refresh_token
from src.models.professor_model import Professor
from src.exceptions.custom_exception import CustomException, ErrorType

def authenticate_professor(professor_service, email, senha):
    professor = professor_service.login_professor(email, senha)
    if professor:
        access_token = create_access_token(identity=str(professor.id))
        return access_token
    else:
        return None