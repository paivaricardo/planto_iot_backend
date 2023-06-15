import logging
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.autorizacao_sensor_model import AutorizacaoSensor
from model.sensor_atuador_model import SensorAtuador


def verificar_existencia_sensor_atuador_base_dados(uuid_informado: UUID):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Buscar se há uma correspondência do UUID informado para um atuador na base de dados
        sensor_atuador = session.query(SensorAtuador).filter(
            SensorAtuador.uuid_sensor_atuador == str(uuid_informado)).first()

        try:
            sensor_atuador_cadastrado = bool(
                sensor_atuador.nome_sensor and
                sensor_atuador.latitude and
                sensor_atuador.longitude and
                sensor_atuador.data_cadastro_sensor and
                sensor_atuador.id_usuario_cadastrante and
                sensor_atuador.id_area and
                sensor_atuador.id_cultura and
                sensor_atuador.id_tipo_sensor
            )
        except Exception as e:
            sensor_atuador_cadastrado = False

        # Consultar todas as autorizações para determinado sensor ou atuador
        autorizacoes_info = []

        if sensor_atuador:
            autorizacoes = session.query(AutorizacaoSensor).filter(
                AutorizacaoSensor.id_sensor_atuador == sensor_atuador.id_sensor_atuador
            ).all()

            for autorizacao in autorizacoes:
                autorizacao_info = {
                    "id_autorizacao_sensor": autorizacao.id_autorizacao_sensor,
                    "id_sensor_atuador": autorizacao.id_sensor_atuador,
                    "usuario": autorizacao.usuario,
                    "perfil_autorizacao": autorizacao.perfil_autorizacao,
                    "visualizacao_ativa": autorizacao.visualizacao_ativa
                }

                autorizacoes_info.append(autorizacao_info)

        if not sensor_atuador:
            logging.info(
                f"[DAO - INFO] Sensor ou atuador com o UUID {uuid_informado} não encontrado no banco de dados.")
            return {"sensor_atuador_existe_bd": False, "sensor_atuador_foi_cadastrado": False,
                    "sensor_atuador_info": None, "autorizacoes": None}
        if not sensor_atuador_cadastrado:
            logging.info(
                f"[DAO - INFO] Sensor ou atuador com o UUID {uuid_informado} foi encontrado no banco de dados, porém ainda não foi cadastrado.")
            return {"sensor_atuador_existe_bd": True, "sensor_atuador_foi_cadastrado": False,
                    "sensor_atuador_info": sensor_atuador, "autorizacoes": autorizacoes_info}
        else:
            return {"sensor_atuador_existe_bd": True, "sensor_atuador_foi_cadastrado": True,
                    "sensor_atuador_info": sensor_atuador, "autorizacoes": autorizacoes_info}
    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao verificar se o atuador existe na base de dados: {str(e)}")
        raise Exception("Erro ao verificar se o atuador existe na base de dados", str(e))
    finally:
        session.close()
