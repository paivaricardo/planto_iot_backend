import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.autorizacao_sensor_model import AutorizacaoSensor
from model.pydantic_rest_models.autorizacao_pydantic_model import AutorizacaoPydanticModel


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


def criar_autorizacao_bd(autorizacao_pydantic_model: AutorizacaoPydanticModel, id_usuario: int):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:
        # Instanciar um objeto de autorização
        autorizacao = AutorizacaoSensor(id_sensor_atuador=autorizacao_pydantic_model.id_sensor_atuador,
                                        id_usuario=id_usuario,
                                        id_perfil_autorizacao=autorizacao_pydantic_model.id_perfil_autorizacao,
                                        visualizacao_ativa=autorizacao_pydantic_model.conectar)

        # Adicionar o objeto de autorização à sessão
        session.add(autorizacao)

        # Comitar a sessão
        session.commit()

        autorizacao_dict = {
            "id_autorizacao_sensor": autorizacao.id_autorizacao_sensor,
            "id_sensor_atuador": autorizacao.id_sensor_atuador,
            "id_usuario": autorizacao.id_usuario,
            "id_perfil_autorizacao": autorizacao.id_perfil_autorizacao,
            "visualizacao_ativa": autorizacao.visualizacao_ativa,
        }

        return autorizacao_dict

    except SQLAlchemyError as e:
        session.rollback()

        logging.error(f"[DAO - ERRO] Erro ao tentar criar autorização: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao tentar criar autorização: {str(e)}")
    finally:
        session.close()
