--Tables:
CREATE TABLE cliente (
id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
nome       VARCHAR(30) NOT NULL,
telefone   VARCHAR(30),
nascimento DATE,
password   VARCHAR(30) NOT NULL
);

CREATE TABLE construcao(
id_construcao INTEGER PRIMARY KEY AUTOINCREMENT,
id_cidade     INT NOT NULL,
id_cliente    INT NOT NULL,
nome          VARCHAR(30) NOT NULL,
altura_maxima NUMERIC(6,2), --Em metros
altura_minima NUMERIC(6,2), --Em metros
bairro        VARCHAR(30) NOT NULL,
cep           VARCHAR(30) NOT NULL,
FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente),
FOREIGN KEY(id_cidade) REFERENCES cidade(id_cidade)
);


CREATE TABLE cidade(
id_cidade INTEGER PRIMARY KEY AUTOINCREMENT,
id_regiao INT NOT NULL,
nome      VARCHAR(30) NOT NULL,
FOREIGN KEY(id_regiao) REFERENCES regiao(id_regiao)
);

CREATE TABLE regiao(
id_regiao INTEGER PRIMARY KEY AUTOINCREMENT,
id_pais   INT NOT NULL,
nome      VARCHAR(30) NOT NULL,
FOREIGN KEY(id_pais) REFERENCES pais(id_pais)
);

CREATE TABLE pais(
id_pais INTEGER PRIMARY KEY AUTOINCREMENT,
nome    VARCHAR(30) NOT NULL
);


CREATE TABLE inspecao(
id_inspecao   INTEGER PRIMARY KEY AUTOINCREMENT,
id_construcao INT NOT NULL,
data_inicio   DATETIME NOT NULL,
data_fim      DATETIME,
analisado     BOOLEAN DEFAULT FALSE,
FOREIGN KEY(id_construcao) REFERENCES construcao(id_construcao)
);

CREATE TABLE imagens_inspecao(
id_imagens_inspecao INTEGER PRIMARY KEY AUTOINCREMENT,
id_inspecao         INT NOT NULL,
nome                VARCHAR(30) NOT NULL,
endereco            VARCHAR(50) NOT NULL,
label               VARCHAR(10),
latitude            NUMERIC(4,2),
longitude           NUMERIC(4,2),
data_criacao        DATETIME  NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP,'localtime')),
FOREIGN KEY(id_inspecao) REFERENCES inspecao(id_inspecao)
);


CREATE TABLE drone(
id_drone       INTEGER PRIMARY KEY AUTOINCREMENT,
id_modelo      INT NOT NULL,
nome           VARCHAR(30) NOT NULL,
data_aquisicao DATE,
custo_compra   NUMERIC(6, 2),
FOREIGN KEY(id_modelo) REFERENCES modelo(id_modelo)
);


CREATE TABLE modelo(
id_modelo          INTEGER PRIMARY KEY AUTOINCREMENT,
id_marca           INT NOT NULL,
nome               VARCHAR(30) NOT NULL,
altura_maxima      NUMERIC(6, 2), -- em metros.
autonomia_voo      NUMERIC(6, 2), -- em minutos. 
distancia_controle NUMERIC(6, 2), -- em metros. 
FOREIGN KEY(id_marca) REFERENCES marca(id_marca)
);

CREATE TABLE marca(
id_marca INTEGER PRIMARY KEY AUTOINCREMENT,
nome     VARCHAR(30) NOT NULL
);

CREATE TABLE drone_compor_inspecao(
id_drone           INT NOT NULL,
id_inspecao        INT NOT NULL,
FOREIGN KEY(id_drone) REFERENCES drone(id_drone),
FOREIGN KEY(id_inspecao) REFERENCES inspecao(id_inspecao),
PRIMARY KEY(id_drone, id_inspecao)
);

CREATE TABLE imagens_treinamento(
id_imagens_treinamento INTEGER PRIMARY KEY AUTOINCREMENT,
nome                VARCHAR(30) NOT NULL,
endereco            VARCHAR(50) NOT NULL,
label               VARCHAR(10),
data_criacao        DATETIME  NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP,'localtime'))
);
