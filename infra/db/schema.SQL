-- Schema recomendado para PostgreSQL

-- tabela de professores
CREATE TABLE professores (
    id              BIGSERIAL PRIMARY KEY,
    nome            VARCHAR(255) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    senha_hash      VARCHAR(255) NOT NULL,
    criado_em       TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- tabela de laboratorios
CREATE TABLE laboratorios (
    id              BIGSERIAL PRIMARY KEY,
    nome            VARCHAR(255) NOT NULL,
    capacidade      INTEGER NOT NULL CHECK (capacidade >= 0),
    criado_em       TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- tabela de agendamentos
CREATE TABLE agendamentos (
    id              BIGSERIAL PRIMARY KEY,
    id_laboratorio  BIGINT NOT NULL REFERENCES laboratorios(id) ON DELETE CASCADE,
    id_professor    BIGINT NOT NULL REFERENCES professores(id) ON DELETE CASCADE,
    data_agendamento DATE NOT NULL, -- data do agendamento (apenas data)
    hora_inicio     TIME NOT NULL,
    hora_fim        TIME NOT NULL,
    criado_em       TIMESTAMP WITH TIME ZONE DEFAULT now(),
    CONSTRAINT chk_horario_valido CHECK (hora_fim > hora_inicio)
);

-- Índices úteis
CREATE INDEX idx_agendamentos_labs_data ON agendamentos (id_laboratorio, data_agendamento);
CREATE INDEX idx_agendamentos_prof_data ON agendamentos (id_professor, data_agendamento);
