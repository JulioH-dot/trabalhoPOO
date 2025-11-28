class Agendamento:
    def __init__(self, id, id_laboratorio, id_professor, data_agendamento, hora_inicio, hora_fim, criado_em=''):
        self.id = id
        self.id_laboratorio = id_laboratorio
        self.id_professor = id_professor
        self.data_agendamento = data_agendamento
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.criado_em = criado_em
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_laboratorio': self.id_laboratorio,
            'id_professor': self.id_professor,
            'data_agendamento': self.data_agendamento,
            'hora_inicio': self.hora_inicio,
            'hora_fim': self.hora_fim
        }