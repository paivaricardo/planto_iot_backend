import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.sensor_atuador_model import SensorAtuador


def verificar_existencia_sensor_atuador_base_dados(uuid_informado: str):
    try:
        # Criar uma sessão para acesso ao banco de dados
        session = database.create_session()

        # Buscar se há uma correspondência do UUID informado para um atuador na base de dados
        sensor_atuador = session.query(SensorAtuador).filter(SensorAtuador.uuid_sensor_atuador == uuid_informado).first()

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

        if not sensor_atuador:
            logging.info(f"[DAO - INFO] Sensor ou atuador com o UUID {uuid_informado} não encontrado no banco de dados.")
            return {"sensor_atuador_existe_bd": False, "sensor_atuador_foi_cadastrado": False, "sensor_atuador_info": None}
        if not sensor_atuador_cadastrado:
            logging.info(f"[DAO - INFO] Sensor ou atuador com o UUID {uuid_informado} foi encontrado no banco de dados, porém ainda não foi cadastrado.")
            return {"sensor_atuador_existe_bd": True, "sensor_atuador_foi_cadastrado": False, "sensor_atuador_info": sensor_atuador}
        else:
            return {"sensor_atuador_existe_bd": True, "sensor_atuador_foi_cadastrado": True, "sensor_atuador_info": sensor_atuador}

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao verificar se o atuador existe na base de dados: {str(e)}")
        raise Exception("Erro ao verificar se o atuador existe na base de dados", str(e))