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
                    conn.commit()
                    return cursor.fetchone()[0]
        except IntegrityError as e:
            raise CustomException(ErrorType.INVALID_OPERATION, "Já existe um agendamento para o mesmo laboratório e horário.")

    def fazer_agendamento(self, agendamento):
        horario_inicio = datetime.strptime("08:00", "%H:%M")
        horario_fim = datetime.strptime("22:00", "%H:%M")
        horario_atual = horario_inicio

        while horario_atual + timedelta(hours=1) <= horario_fim:
            if self.existe_agendamento_no_intervalo(agendamento.id_laboratorio, agendamento.data, horario_atual - timedelta(minutes=15), horario_atual + timedelta(hours=1)):
                # Verifica se existe algum agendamento dentro do intervalo de 15 minutos antes e depois do horário atual
                if not self.existe_agendamento_no_intervalo(agendamento.id_laboratorio, agendamento.data, horario_atual - timedelta(minutes=15), horario_atual + timedelta(hours=1)):
                    agendamento = Agendamento(
                        None,
                        id_laboratorio=agendamento.id_laboratorio,
                        id_professor=agendamento.id_professor,
                        data=agendamento.data,
                        hora_inicio=horario_atual,
                        hora_fim=horario_atual + timedelta(hours=1)
                    )
                    self.create(agendamento)
                    return agendamento
            horario_atual += timedelta(minutes=15)
        
        raise CustomException(ErrorType.INVALID_OPERATION, "Nenhum horário disponível para agendamento")

    def existe_agendamento_no_intervalo(self, id_laboratorio, data, inicio, fim):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                sql = """
                SELECT COUNT(*) FROM Agendamento 
                WHERE id_laboratorio = %s 
                AND data = %s 
                AND hora_inicio::time >= %s::time 
                AND hora_fim::time <= %s::time
                """
                cursor.execute(sql, (id_laboratorio, data, str(inicio), str(fim)))
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
