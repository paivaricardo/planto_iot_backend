import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.usuario_model import Usuario


def obter_usuarios_bd():
    session = database.create_session()

    try:
        return session.query(Usuario).all()

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao obter todas os usuários: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao obter todas os usuários: {str(e)}")

    finally:
        session.close()