import logging

from sqlalchemy.exc import SQLAlchemyError
from mdl_dao import database
from model.cultura_model import Cultura


def obter_todas_culturas():
    session = database.create_session()

    try:
        return session.query(Cultura).all()

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao obter todas as culturas: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao obter todas as culturas: {str(e)}")

    finally:
        session.close()
