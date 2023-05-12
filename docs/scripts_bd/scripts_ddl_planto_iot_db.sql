-- ************************************** PRE_REQS (para PostgreSQL)
CREATE USER planto_iot_user WITH PASSWORD ‘planto-iot’;
ALTER USER planto_iot_user WITH CREATEDB;
CREATE DATABASE db_planto_iot_sensores;




-- ************************************** tb_sensor_atuador
CREATE TABLE tb_sensor_atuador
(
   id_sensor_atuador int NOT NULL GENERATED ALWAYS AS IDENTITY,
   uuid_sensor_atuador varchar(255) NOT NULL,
   nome_sensor varchar(50) NULL,
   latitude float NULL,
   longitude float NULL,
   data_cadastro_sensor date NULL,
   data_precadastro_sensor date NOT NULL,
   id_usuario_cadastrante int NULL,
   id_area int NULL,
   id_cultura int NULL,
   id_tipo_sensor int NOT NULL,
   CONSTRAINT PK_tb_sensor_atuador PRIMARY KEY (id_sensor_atuador),
   CONSTRAINT IDX_UUID_SENSOR UNIQUE (uuid_sensor_atuador)
);


CREATE INDEX FK_id_usuario_cadastrante_tb_sensor_atuador ON
   tb_sensor_atuador
       (id_usuario_cadastrante);


CREATE INDEX FK_id_area_tb_sensor_atuador ON
   tb_sensor_atuador
       (id_area);


CREATE INDEX FK_id_cultura_tb_sensor_atuador ON
   tb_sensor_atuador
       (id_cultura);


CREATE INDEX FK_id_tipo_sensor_tb_sensor_atuador ON
   tb_sensor_atuador
       (id_tipo_sensor);




-- ************************************** tb_tipo_sensor


CREATE TABLE tb_tipo_sensor
(
   id_tipo_sensor int NOT NULL GENERATED ALWAYS AS IDENTITY,
   nome_tipo_sensor varchar(50) NOT NULL,
   CONSTRAINT PK_tb_tipo_sensor PRIMARY KEY (id_tipo_sensor)
);




-- ************************************** tb_tipo_sinal


CREATE TABLE tb_tipo_sinal
(
   id_tipo_sinal int NOT NULL GENERATED ALWAYS AS IDENTITY,
   nome_tipo_sinal varchar(20) NOT NULL,
   CONSTRAINT PK_tb_tipo_sinal PRIMARY KEY (id_tipo_sinal)
);




-- ************************************** tb_usuario


CREATE TABLE tb_usuario
(
   id_usuario int NOT NULL GENERATED ALWAYS AS IDENTITY,
   email_usuario varchar(50) NOT NULL,
   nome_usuario varchar(100) NOT NULL,
   data_cadastro date NOT NULL,
   id_perfil int NOT NULL,
   CONSTRAINT PK_tb_usuario PRIMARY KEY (id_usuario)
);


CREATE INDEX FK_id_perfil_tb_usuario ON
   tb_usuario (id_perfil);




-- ************************************** tb_area


CREATE TABLE tb_area
(
   id_area int NOT NULL GENERATED ALWAYS AS IDENTITY,
   nome_area varchar(30) NOT NULL,
   CONSTRAINT PK_tb_area PRIMARY KEY (id_area)
);




-- ************************************** tb_cultura
CREATE TABLE tb_cultura
(
   id_cultura int NOT NULL GENERATED ALWAYS AS IDENTITY,
   nome_cultura varchar(30) NOT NULL,
   CONSTRAINT PK_tb_cultura PRIMARY KEY (id_cultura)
);




-- ************************************** tb_leitura_atuacao


CREATE TABLE tb_leitura_atuacao
(
   id_leitura_atuacao int NOT NULL GENERATED ALWAYS AS IDENTITY,
   data_hora_leitura timestamp WITH time ZONE NOT NULL,
   json_leitura TEXT NULL,
   id_sensor_atuador int NOT NULL,
   id_tipo_sinal int NOT NULL,
   CONSTRAINT PK_tb_leitura_atuacao PRIMARY KEY (id_leitura_atuacao)
);


CREATE INDEX FK_id_sensor_atuador_tb_leitura_atuaca ON
   tb_leitura_atuacao
       (id_sensor_atuador);


CREATE INDEX FK_id_tipo_sinal_tb_leitura_atuaca ON
   tb_leitura_atuacao
       (id_tipo_sinal);




-- ************************************** tb_perfil

CREATE TABLE tb_perfil
(
   id_perfil int NOT NULL GENERATED ALWAYS AS IDENTITY,
   nome_perfil varchar(50) NOT NULL,
   CONSTRAINT PK_tb_perfil PRIMARY KEY (id_perfil)
);


-- CHAVES ESTRANGEIRAS




-- ************************************** tb_sensor_atuador
ALTER TABLE tb_sensor_atuador
   ADD CONSTRAINT FK_id_usuario_cadastrante_tb_sensor_atuador FOREIGN KEY (id_usuario_cadastrante) REFERENCES tb_usuario (id_usuario),
   ADD CONSTRAINT FK_id_area_tb_sensor_atuador FOREIGN KEY (id_area) REFERENCES tb_area (id_area),
   ADD CONSTRAINT FK_id_cultura_tb_sensor_atuador FOREIGN KEY (id_cultura) REFERENCES tb_cultura (id_cultura),
   ADD CONSTRAINT FK_id_tipo_sensor_tb_sensor_atuador FOREIGN KEY (id_tipo_sensor) REFERENCES tb_tipo_sensor (id_tipo_sensor);




-- ************************************** tb_leitura_atuacao
ALTER TABLE tb_leitura_atuacao
   ADD CONSTRAINT FK_7 FOREIGN KEY (id_tipo_sinal) REFERENCES tb_tipo_sinal (id_tipo_sinal);




-- ************************************** tb_usuario
ALTER TABLE tb_usuario
   ADD CONSTRAINT FK_2_1 FOREIGN KEY (id_perfil) REFERENCES tb_perfil (id_perfil);
