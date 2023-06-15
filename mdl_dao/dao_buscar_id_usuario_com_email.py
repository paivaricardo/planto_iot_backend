import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.usuario_model import Usuario


def buscar_id_usuario_com_email(email_usuario: str):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Buscar o usuário correspondente ao email informado
        id_usuario = session.query(Usuario.id_usuario).filter(Usuario.email_usuario == email_usuario).first()

        if id_usuario:
            return id_usuario[0]
        else:
            return None

    except SQLAlchemyError as e:
        logging.error(
            f"[DAO - ERRO] Erro ao tentar obter o id do usuário com email {email_usuario}: {str(e)}")
        raise Exception(
            f"[DAO - ERRO] Erro ao tentar obter o id do usuário com email {email_usuario}: {str(e)}")
    finally:
        session.close()
