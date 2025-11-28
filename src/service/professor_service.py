import bcrypt
from src.models.professor_model import Professor
from src.enums.enum import ErrorType
from src.exceptions.custom_exception import CustomException
from src.service.validarEmail import validate_email
from datetime import datetime

class ProfessorService:
    def __init__(self, professor_repository):
        self.professor_repository = professor_repository

    def hash_password(self, senha):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')

    def criar_professor(self, nome, email, senha):
        if not nome or not email or not senha:
            raise CustomException(ErrorType.INVALID_EMAIL, "Nome, email e senha são obrigatórios.")

        senha_hash = self.hash_password(senha)
        
        criado_em = datetime.now()
        
        try:
            validate_email(email)
            id = self.professor_repository.create(Professor(None, nome, email, senha_hash, criado_em)) 
            return id
        
        except Exception as e:
            raise e

    def busca_professor_id(self, id):
        try:
            professor =  self.professor_repository.get_by_id(id)
            
            return {
                "id": professor.id,
                "nome": professor.nome,
                "email": professor.email
            }

        except Exception:
            raise CustomException(ErrorType.NOT_FOUND, f"Professor com ID {id} não encontrado.")

    def listar_professores(self):
        try:
            return self.professor_repository.get_all()
        
        except Exception:
            raise CustomException(ErrorType.DATABASE_ERROR, "Erro ao listar os professores, erro genérico na busca destes elementos")


    def atualizar_professor(self, id, nome, email, senha):

        if not self.professor_repository.get_by_id(id):

            raise CustomException(ErrorType.NOT_FOUND, f"Professor com ID {id} não encontrado.")
        
        try:
            return self.professor_repository.update(Professor(id, nome, email, senha))

        except Exception:
            raise CustomException(ErrorType.DATABASE_ERROR, f"Erro ao atualizar o professor com o ID {id}")

    def deletar_professor(self, id):
        if not self.professor_repository.get_by_id(id):
            raise CustomException(ErrorType.NOT_FOUND, f"Professor com ID {id} não encontrado.")

        try:
            return self.professor_repository.delete(id)
        except Exception as e:
            CustomException(ErrorType.DATABASE_ERROR, f"Erro ao deletar o professor com o ID {id}")

    def login_professor(self, email, senha):
        professor = self.professor_repository.get_by_email(email)
        if professor: 
            try:
                is_valid = bcrypt.checkpw(
                    senha.encode('utf-8'), 
                    professor.senha.encode('utf-8')
                )
                if is_valid:
                    return professor
                else: 
                    raise None
            except ValueError:
                return None
        else:
            return None

