# src/services/agendamento_service.py

from datetime import datetime, timedelta
from src.models.agendamento_model import Agendamento
from src.exceptions.custom_exception import CustomException
from src.enums.enum import ErrorType

class AgendamentoService:
    def __init__(self, agendamento_repository):
        self.agendamento_repository = agendamento_repository

    def create_agendamento(self, id_laboratorio, id_professor, data, hora_inicio, hora_fim):
        if not id_laboratorio or not id_professor or not data or not hora_inicio or not hora_fim:
            raise CustomException(ErrorType.INVALID_OPERATION, "All fields are required")

        # Validação da hora_inicio e hora_fim
        hora_inicio_dt = datetime.strptime(hora_inicio, '%H:%M')
        hora_fim_dt = datetime.strptime(hora_fim, '%H:%M')

        # Verificação da duração do agendamento (1h por padrão)
        if (hora_fim_dt - hora_inicio_dt).total_seconds() / 3600 != 1:
            raise CustomException(ErrorType.INVALID_OPERATION, "Each appointment must be 1 hour long")

        # Criação do agendamento
        agendamento = Agendamento(
            id=None,
            id_laboratorio=id_laboratorio,
            id_professor=id_professor,
            data_agendamento=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            criado_em=None
        )
        return self.agendamento_repository.fazer_agendamento(agendamento)

    def get_all_agendamentos(self):
        return self.agendamento_repository.get_all()

    def get_agendamento_by_id(self, agendamento_id):
        if not agendamento_id:
            raise CustomException(ErrorType.INVALID_EMAIL, "Agendamento ID is required")
        return self.agendamento_repository.get_by_id(agendamento_id)

    def update_agendamento(self, agendamento_id, id_laboratorio, id_professor, data, hora_inicio, hora_fim):
        if not agendamento_id or not id_laboratorio or not id_professor or not data or not hora_inicio or not hora_fim:
            raise CustomException(ErrorType.INVALID_OPERATION, "All fields are required")
        agendamento = Agendamento(
            id=agendamento_id,
            id_laboratorio=id_laboratorio,
            id_professor=id_professor,
            data=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )
        self.agendamento_repository.update(agendamento)

    def delete_agendamento(self, agendamento_id):
        if not agendamento_id:
            raise CustomException(ErrorType.INVALID_EMAIL, "Agendamento ID is required")
        self.agendamento_repository.delete(agendamento_id)
