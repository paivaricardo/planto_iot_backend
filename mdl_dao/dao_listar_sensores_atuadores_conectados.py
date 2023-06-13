import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.autorizacao_sensor_model import AutorizacaoSensor
from model.query_models.sensor_atuador_query_model import SensorAtuadorQueryModel


def listar_sensores_atuadores_conectados_bd(id_usuario):
    try:
        # Criar uma sessão para acesso ao banco de dados
        session = database.create_session()

        # Subquery para buscar os sensores e atuadores que o usuário tem permissão de visualizar
        subquery_sensores_atuadores_permissao_visualizacao = session.query(AutorizacaoSensor.id_sensor_atuador).filter(
            AutorizacaoSensor.visualizacao_ativa == True,
            AutorizacaoSensor.id_usuario == id_usuario
        ).subquery()

        # Query para buscar os sensores e atuadores que estão presentes na subquery acima
        sensores_atuadores_permissao_visualizacao = session.query(SensorAtuadorQueryModel).filter(
            SensorAtuadorQueryModel.id_sensor_atuador.in_(subquery_sensores_atuadores_permissao_visualizacao)
        ).all()

        if sensores_atuadores_permissao_visualizacao is None:
            return []
        else:
            return sensores_atuadores_permissao_visualizacao

    except SQLAlchemyError as e:
        logging.error(
            f"[DAO - ERRO] Erro ao tentar obter a lista de sensores e atuadores que o usuário de id {id_usuario} possui permissão de acesso: {str(e)}")
        raise Exception(
            f"[DAO - ERRO] Erro ao tentar obter a lista de sensores e atuadores que o usuário de id {id_usuario} possui permissão de acesso: {str(e)}")
    finally:
        session.close()
