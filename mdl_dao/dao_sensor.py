import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.query_models.sensor_atuador_query_model import SensorAtuadorQueryModel


def obter_sensores_bd():
    session = database.create_session()

    try:
        sensores = session.query(SensorAtuadorQueryModel).all()
        return sensores

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao obter todas os sensores: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao obter todas os sensores: {str(e)}")

    finally:
        session.close()
