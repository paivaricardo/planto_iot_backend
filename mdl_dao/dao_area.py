import logging

from sqlalchemy.exc import SQLAlchemyError
from mdl_dao import database
from model.area_model import Area


def obter_todas_areas():
    session = database.create_session()

    try:
        return session.query(Area).all()

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao obter todas as áreas: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao obter todas as áreas: {str(e)}")

    finally:
        session.close()
