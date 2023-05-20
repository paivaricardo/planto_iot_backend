import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.sensor_atuador_model import SensorAtuador


def verificar_existencia_atuador_base_dados(uuid_informado: str):
    try:
        # Criar uma sessão para acesso ao banco de dados
        session = database.create_session()

        # Buscar se há uma correspondência do UUID informado para um atuador na base de dados
        atuador = session.query(SensorAtuador).filter(SensorAtuador.uuid_sensor_atuador == uuid_informado).first()

        if not atuador:
            logging.info(f"[DAO - INFO] Atuador com o UUID {uuid_informado} não encontrado no banco de dados.")
            return False
        else:
            logging.info(f"[DAO - INFO] Atuador com o UUID {uuid_informado} foi encontrado no banco de dados.")
            return True

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao verificar se o atuador existe na base de dados: {str(e)}")
        raise Exception("Erro ao verificar se o atuador existe na base de dados", str(e))