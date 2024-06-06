class Agendamento:
    def __init__(self, id, id_laboratorio, id_professor, data, hora_inicio, hora_fim):
        self.id = id
        self.id_laboratorio = id_laboratorio
        self.id_professor = id_professor
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_laboratorio': self.id_laboratorio,
            'id_professor': self.id_professor,
            'data': self.data,
            'hora_inicio': self.hora_inicio,
            'hora_fim': self.hora_fim
        }