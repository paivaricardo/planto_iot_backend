import datetime
import json
import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.log_model import Log
from model.usuario_model import Usuario


def registrar_login_usuario_log_bd(id_usuario):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Buscar o usuário associado ao id
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

        json_log = {
            "id_usuario": usuario.id_usuario,
            "nome_usuario": usuario.nome_usuario,
            "email_usuario": usuario.email_usuario,
            "data_hora_login": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            "mensagem": f"O usuário {usuario.nome_usuario} - email {usuario.email_usuario} realizou login no sistema às {datetime.datetime.now()}"
        }

        # Criar uma nova instância do modelo LeituraAtuacao
        log = Log(
            data_hora_log=datetime.datetime.now(),
            json_log=json.dumps(json_log),
            id_usuario=usuario.id_usuario,
            id_log_event_type=1
        )

        # Persist the LeituraAtuacao object in the database
        session.add(log)
        session.commit()

        logging.info(f"[LOG - DAO - INFO] - Login do usuário {usuario.nome_usuario} - email: {usuario.email_usuario} registrado com sucesso no banco de dados.")
    except SQLAlchemyError as e:
        session.rollback()
        # Handle the exception as needed
        logging.error(f"[LOG - DAO -ERRO] Error occurred while persisting sensor reading: {str(e)}")

    finally:
        session.close()
