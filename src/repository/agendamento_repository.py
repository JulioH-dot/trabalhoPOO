# src/repositories/agendamento_repository.py

from datetime import datetime, timedelta
from src.models.agendamento_model import Agendamento
from src.exceptions.custom_exception import CustomException
from src.enums.enum import ErrorType
from psycopg2 import IntegrityError

class AgendamentoRepository:
    def __init__(self, database):
        self.database = database


    def create(self, agendamento):
        try:
            with self.database.connect() as conn:
                with conn.cursor() as cursor:
                    sql = """
                    INSERT INTO Agendamento (id_laboratorio, id_professor, data, hora_inicio, hora_fim)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                    """
                    cursor.execute(sql, (agendamento.id_laboratorio, agendamento.id_professor, agendamento.data, agendamento.hora_inicio, agendamento.hora_fim))
                    agendamento_id = cursor.fetchone()[0]
                    conn.commit()
                    return agendamento_id
        except IntegrityError as e:
            raise CustomException(ErrorType.INVALID_OPERATION, "Já existe um agendamento para o mesmo laboratório e horário.")

    def fazer_agendamento(self, agendamento):
        horario_inicio = datetime.strptime(agendamento.hora_inicio, "%H:%M").time()
        horario_fim = datetime.strptime(agendamento.hora_fim, "%H:%M").time()

        # Ajusta horários para considerar intervalo de 15 minutos
        inicio_intervalo = (datetime.combine(datetime.today(), horario_inicio) - timedelta(minutes=15)).time()
        fim_intervalo = (datetime.combine(datetime.today(), horario_fim) + timedelta(minutes=15)).time()

        # Verifica se o horário especificado está disponível
        if self.existe_agendamento_no_intervalo(agendamento.id_laboratorio, agendamento.data, inicio_intervalo, fim_intervalo):
            raise CustomException(ErrorType.INVALID_OPERATION, "O horário especificado não está disponível")

        agendamento_id = self.create(agendamento)
        return {"id": agendamento_id, "mensagem": "Agendamento criado com sucesso."}


    def existe_agendamento_no_intervalo(self, id_laboratorio, data, inicio, fim):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                sql = """
                SELECT COUNT(*) FROM Agendamento 
                WHERE id_laboratorio = %s 
                AND data = %s 
                AND (hora_inicio < %s::time AND hora_fim > %s::time)
                """
                cursor.execute(sql, (id_laboratorio, data, fim, inicio))
                return cursor.fetchone()[0] > 0

    def get_all(self):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Agendamento")
                return [Agendamento(*row) for row in cursor.fetchall()]

    def get_by_id(self, agendamento_id):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Agendamento WHERE id = %s", (agendamento_id,))
                agendamento = cursor.fetchone()
                if not agendamento:
                    raise CustomException(ErrorType.NOT_FOUND, f"Agendamento with id {agendamento_id} not found")
                return Agendamento(*agendamento)

    def update(self, agendamento):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                sql = """
                UPDATE Agendamento SET id_laboratorio = %s, id_professor = %s, data = %s, hora_inicio = %s, hora_fim = %s
                WHERE id = %s
                """
                cursor.execute(sql, (agendamento.id_laboratorio, agendamento.id_professor, agendamento.data, agendamento.hora_inicio, agendamento.hora_fim, agendamento.id))
                conn.commit()

    def delete(self, agendamento_id):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Agendamento WHERE id = %s", (agendamento_id,))
                if cursor.rowcount == 0:
                    raise CustomException(ErrorType.NOT_FOUND, f"Agendamento with id {agendamento_id} not found")
                conn.commit()
