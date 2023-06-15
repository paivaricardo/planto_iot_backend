import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.autorizacao_sensor_model import AutorizacaoSensor
from model.sensor_atuador_model import SensorAtuador
from model.usuario_model import Usuario


def verificar_autorizacao_acesso_sensor_database(uuid_sensor: str, email_usuario: str):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Buscar se há um usuário correspondente ao email informado na base de dados
        usuario = session.query(Usuario).filter(
            Usuario.email_usuario == email_usuario).first()

        # Se não for localizado usuário, retornar que o usuário não está autorizado e não foi encontrado
        if not usuario:
            logging.info(
                f"[DAO - INFO] Não há usuário correspondente ao email {email_usuario}.")
            return {"usuario_autorizado": False, "perfil_autorizacao": None}

        # Buscar se há um sensor correspondente ao UUID informado na base de dados
        sensor_atuador = session.query(SensorAtuador).filter(
            SensorAtuador.uuid_sensor_atuador == uuid_sensor).first()

        # Se não for localizado sensor, retornar que o usuário não está autorizado e não foi encontrado
        if not sensor_atuador:
            logging.info(
                f"[DAO - INFO] Não há sensor correspondente ao UUID {uuid_sensor}.")
            return {"usuario_autorizado": False, "perfil_autorizacao": None}

        # Verificar se o usuário tem autorização para acessar o sensor
        status_autorizacao_sensor = session.query(AutorizacaoSensor).filter(
            AutorizacaoSensor.id_usuario == usuario.id_usuario, AutorizacaoSensor.id_sensor_atuador == sensor_atuador.id_sensor_atuador).first()

        # Se não for localizada autorização, retornar que o usuário não está autorizado e não foi encontrado
        if not status_autorizacao_sensor:
            logging.info(
                f"[DAO - INFO] Não há autorização para o usuário acessar o sensor com UUID {uuid_sensor}.")
            return {"usuario_autorizado": False, "perfil_autorizacao": None}

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao verificar se o atuador existe na base de dados: {str(e)}")
        raise Exception("Erro ao verificar se o atuador existe na base de dados", str(e))
    finally:
        session.close()
