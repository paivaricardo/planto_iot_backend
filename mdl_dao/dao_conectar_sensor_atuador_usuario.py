import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.autorizacao_sensor_model import AutorizacaoSensor


def conectar_sensor_atuador_usuario_dao(autorizacao_usuario):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Buscar se há uma correspondência do id da autorizacao para uma autorizacao na base de dados
        autorizacao_usuario_database = session.query(AutorizacaoSensor).filter(
            AutorizacaoSensor.id_autorizacao_sensor == autorizacao_usuario["id_autorizacao_sensor"]).first()

        # Atualizar a autorização, para constar visualização ativa como True (isso representa uma conexão àquele usuário)
        autorizacao_usuario_database.visualizacao_ativa = True

        # Fazer o update com base nas novas informações de cadastro fornecidas
        session.add(autorizacao_usuario_database)

        # Fazer o commit das alterações no banco de dados
        session.commit()

        logging.info(
            f"[DAO - INFO] Sensor ou atuador de id {autorizacao_usuario['id_sensor_atuador']} conectado ao usuário de id {autorizacao_usuario['usuario'].id_usuario} com sucesso")

        return True

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao tentar conectar o usuário ao sensor/atuador de id {autorizacao_usuario.id_sensor_atuador}: {str(e)}")
        raise Exception(f"Erro ao tentar conectar o usuário ao sensor/atuador de id {autorizacao_usuario.id_sensor_atuador}", str(e))
    finally:
        session.close()
