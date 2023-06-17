from datetime import datetime
import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database, dao_buscar_id_usuario_com_email
from model.pydantic_rest_models.sensor_atuador_cadastro_completo_rest_model import SensorAtuadorCadastroCompleto
from model.sensor_atuador_model import SensorAtuador


def cadastrar_sensor_atuador_base_dados(sensor_atuador_cadastro_completo: SensorAtuadorCadastroCompleto):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:
        # Buscar se há uma correspondência do UUID informado para um sensor ou atuador na base de dados
        sensor_atuador = session.query(SensorAtuador).filter(
            SensorAtuador.uuid_sensor_atuador == str(sensor_atuador_cadastro_completo.uuid_sensor_atuador)).first()

        # Buscar o correspondente id do usuário cadastrante, de acordo com o e-mail informado
        id_usuario_cadastrante = dao_buscar_id_usuario_com_email.buscar_id_usuario_com_email(sensor_atuador_cadastro_completo.email_usuario_cadastrante)

        # Atualizar o sensor ou atuador na base de dados. A data do cadastro será a data atual, gerada pelo DAO
        if sensor_atuador:
            sensor_atuador.nome_sensor = sensor_atuador_cadastro_completo.nome_sensor
            sensor_atuador.latitude = sensor_atuador_cadastro_completo.latitude
            sensor_atuador.longitude = sensor_atuador_cadastro_completo.longitude
            sensor_atuador.data_cadastro_sensor = sensor_atuador.data_cadastro_sensor or datetime.now()
            sensor_atuador.id_usuario_cadastrante = sensor_atuador.id_usuario_cadastrante or id_usuario_cadastrante
            sensor_atuador.id_area = sensor_atuador_cadastro_completo.id_area
            sensor_atuador.id_cultura = sensor_atuador_cadastro_completo.id_cultura
            sensor_atuador.observacoes = sensor_atuador_cadastro_completo.observacoes

        # Fazer o update com base nas novas informações de cadastro fornecidas
        session.add(sensor_atuador)

        # Fazer o commit das alterações no banco de dados
        session.commit()

        logging.info(f"[DAO - INFO] Sensor ou atuador de UUID {str(sensor_atuador.uuid_sensor_atuador)} cadastrado (cadastro completo) com sucesso.")

        return True

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao tentar cadastrar o sensor/atuador de UUID {str(sensor_atuador_cadastro_completo.uuid_sensor_atuador)}: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao tentar cadastrar o sensor/atuador de UUID {str(sensor_atuador_cadastro_completo.uuid_sensor_atuador)}", str(e))
    finally:
        session.close()
