-- Criação da tabela Usuarios
CREATE TABLE Usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    endereco VARCHAR(200),
    telefone VARCHAR(15),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMP
);

-- Criação da tabela Dispositivos
CREATE TABLE Dispositivos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    modelo VARCHAR(100),
    status VARCHAR(20) DEFAULT 'ativo',
    localizacao VARCHAR(200),
    usuario_id INT REFERENCES Usuarios(id) ON DELETE CASCADE,
    data_instalacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da tabela ConsumoEnergia
CREATE TABLE ConsumoEnergia (
    id SERIAL PRIMARY KEY,
    dispositivo_id INT REFERENCES Dispositivos(id) ON DELETE CASCADE,
    data_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_fim TIMESTAMP,
    consumo NUMERIC(10, 2) NOT NULL, -- consumo em kWh
    tarifa NUMERIC(6, 2), -- tarifa cobrada por kWh
    custo_total NUMERIC(10, 2) GENERATED ALWAYS AS (consumo * tarifa) STORED -- custo total calculado
);

-- Criação da tabela Eventos
CREATE TABLE Eventos (
    id SERIAL PRIMARY KEY,
    dispositivo_id INT REFERENCES Dispositivos(id) ON DELETE CASCADE,
    tipo_evento VARCHAR(50) NOT NULL,
    descricao TEXT,
    responsavel VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pendente',
    data_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

