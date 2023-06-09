import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.tipo_sensor_model import TipoSensor


def obter_tipos_sensores_bd():
    session = database.create_session()

    try:
        sensores = session.query(TipoSensor).all()

        sensores_dicts = [{
            'id_tipo_sensor': sensor.id_tipo_sensor,
            'nome_tipo_sensor': sensor.nome_tipo_sensor,
        } for sensor in sensores]

        return sensores_dicts

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao obter os tipos de sensores: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao obter os tipos de sensores: {str(e)}")

    finally:
        session.close()
