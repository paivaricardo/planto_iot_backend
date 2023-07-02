import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.sensor_atuador_model import SensorAtuador


def obter_sensores_bd():
    session = database.create_session()

    try:
        sensores = session.query(SensorAtuador).all()
        return sensores

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao obter todas os sensores: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao obter todas os sensores: {str(e)}")

    finally:
        session.close()
