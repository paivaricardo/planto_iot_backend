-- ************************************** SCRIPTS DML para inserção de dados de domínio do Planto IoT
-- ************************************** Database: db_planto_iot_sensores


-- ************************************** Tabela: tb_perfil
INSERT INTO tb_perfil
    (nome_perfil)
VALUES ('Free'),
       ('Basic'),
       ('Premium'),
       ('Admin');


-- ************************************** Tabela: tb_area
INSERT INTO tb_area
    (nome_area)
VALUES ('Centro Universitário de Brasília - CEUB');


-- ************************************** Tabela: tb_cultura
INSERT INTO tb_cultura
    (nome_cultura)
VALUES ('Tomate Holandês Rama');


-- ************************************** Tabela: tb_tipo_sensor
INSERT INTO tb_tipo_sensor
    (id_tipo_sensor, nome_tipo_sensor)
VALUES (10000, 'Sensor de umidade do solo'),
       (10001, 'Sensor de luminosidade'),
       (10002, 'Sensor de temperatura'),
       (20000, 'Bomba de irrigação de água');


-- ************************************** Tabela: tb_tipo_sinal
INSERT INTO tb_tipo_sinal
    (id_tipo_sinal, nome_tipo_sinal)
VALUES (10000, 'LEITURA'),
       (10001, 'LEITURA-ACK'),
       (20000, 'FALHA'),
       (30000, 'LIGAR'),
       (40000, 'DESLIGAR'),
       (50000, 'ACIONAMENTO'),
       (50001, 'ACIONAMENTO-ACK'),
       (60000, 'CONEXÃO'),
       (60001, 'CONEXÃO-ACK');

-- ************************************** Tabela: tb_perfil_autorizacao
INSERT INTO tb_perfil_autorizacao
    (nme_perfil_autorizacao)
VALUES ('Administrador'),
       ('Usuário');

-- ************************************** Tabela: tb_log_event_type
INSERT INTO tb_log_event_type
    (nome_log_event_type)
VALUES ('USER_LOGIN'),
       ('PRE_REGISTER_SENSOR'),
       ('UPDATE_SENSOR_REGISTER'),
       ('CONNECT_SENSOR'),
       ('DISCONNECT_SENSOR');


