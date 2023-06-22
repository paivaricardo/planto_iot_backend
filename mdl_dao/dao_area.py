import logging

from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError
from mdl_dao import database
from model.area_model import Area
from model.sensor_atuador_model import SensorAtuador


def obter_todas_areas(retrieve_status: bool = False):
    session = database.create_session()

    try:
        areas = None

        if not retrieve_status:
            areas = session.query(Area).all()
        else:
            areas = session.query(Area, exists().where(SensorAtuador.id_area == Area.id_area).label('used')).all()

            for area, used in areas:
                area.deletable = not used

        return areas

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao obter todas as áreas: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao obter todas as áreas: {str(e)}")

    finally:
        session.close()
