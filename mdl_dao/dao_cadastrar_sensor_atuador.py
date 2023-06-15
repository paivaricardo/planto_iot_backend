from datetime import datetime
import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.pydantic_rest_models.sensor_atuador_cadastro_completo_rest_model import SensorAtuadorCadastroCompleto
from model.sensor_atuador_model import SensorAtuador


def cadastrar_sensor_atuador_base_dados(sensor_atuador_cadastro_completo: SensorAtuadorCadastroCompleto):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Buscar se há uma correspondência do UUID informado para um atuador na base de dados
        sensor_atuador = session.query(SensorAtuador).filter(
            SensorAtuador.uuid_sensor_atuador == sensor_atuador_cadastro_completo.uuid_sensor_atuador).first()

        # Atualizar o sensor ou atuador na base de dados. A data do cadastro será a data atual, gerada pelo DAO
        if sensor_atuador:
            sensor_atuador.nome_sensor = sensor_atuador_cadastro_completo.nome_sensor
            sensor_atuador.latitude = sensor_atuador_cadastro_completo.latitude
            sensor_atuador.longitude = sensor_atuador_cadastro_completo.longitude
            sensor_atuador.data_cadastro_sensor = datetime.now()
            sensor_atuador.id_usuario_cadastrante = sensor_atuador_cadastro_completo.id_usuario_cadastrante
            sensor_atuador.id_area = sensor_atuador_cadastro_completo.id_area
            sensor_atuador.id_cultura = sensor_atuador_cadastro_completo.id_cultura

        # Fazer o update com base nas novas informações de cadastro fornecidas
        session.add(sensor_atuador)

        # Fazer o commit das alterações no banco de dados
        session.commit()


        logging.info(f"[DAO - INFO] Sensor ou atuador cadastrado (cadastro completo) com sucesso. Gerado o uuid: {str(sensor_atuador.uuid_sensor_atuador)}")

        return True

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao verificar se o atuador existe na base de dados: {str(e)}")
        raise Exception("Erro ao verificar se o atuador existe na base de dados", str(e))
    finally:
        session.close()
