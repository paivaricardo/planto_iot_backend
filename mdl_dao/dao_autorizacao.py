import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.autorizacao_sensor_model import AutorizacaoSensor


def deletar_autorizacao_bd(id_autorizacao: int):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Buscar o usuário correspondente ao email informado
        autorizacao = session.query(AutorizacaoSensor).filter(
            AutorizacaoSensor.id_autorizacao_sensor == id_autorizacao).first()

        if autorizacao is None:
            raise Exception(f"[DAO - ERRO] Não existe autorização com id {id_autorizacao}")
        else:
            session.delete(autorizacao)
            session.commit()
            return True

    except SQLAlchemyError as e:
        session.rollback()

        logging.error(f"[DAO - ERRO] Erro ao tentar deletar autorização com id {id_autorizacao}: {str(e)}")
        return False
    finally:
        session.close()


def criar_autorizacao_bd(id_sensor_atuador: int, id_usuario: int, id_perfil_autorizacao: int, conectar: bool):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:
        # Instanciar um objeto de autorização
        autorizacao = AutorizacaoSensor(id_sensor_atuador=id_sensor_atuador, id_usuario=id_usuario,
                                        id_perfil_autorizacao=id_perfil_autorizacao, visualizacao_ativa=conectar)

        # Adicionar o objeto de autorização à sessão
        session.add(autorizacao)

        # Comitar a sessão
        session.commit()

    except SQLAlchemyError as e:
        session.rollback()

        logging.error(f"[DAO - ERRO] Erro ao tentar criar autorização: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao tentar criar autorização: {str(e)}")
    finally:
        session.close()
