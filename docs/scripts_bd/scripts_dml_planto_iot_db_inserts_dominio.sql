-- ************************************** SCRIPTS DML para inserção de dados de domínio do Planto IoT
-- ************************************** Database: db_planto_iot_sensores


-- ************************************** Tabela: tb_perfil
INSERT INTO tb_perfil
    (nome_perfil)
VALUES ('Free'),
       ('Basic'),
       ('Premium');


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
VALUES (02000, 'LEITURA'),
       (03000, 'FALHA'),
       (04000, 'LIGAR'),
       (05000, 'DESLIGAR'),
       (06000, 'ACIONAMENTO');

-- ************************************** Tabela: tb_perfil_autorizacao
INSERT INTO tb_perfil_autorizacao
    (nme_perfil_autorizacao)
VALUES ('Administrador'),
       ('Usuário');




