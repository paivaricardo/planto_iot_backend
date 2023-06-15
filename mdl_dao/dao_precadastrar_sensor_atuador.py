import logging
import uuid
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from model.sensor_atuador_model import SensorAtuador
from model.tipo_sensor_model import TipoSensor
from mdl_dao import database


def obter_lista_tipos_sensores_atuadores():
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Fazer consulta na base de dados para todos os tipos de sensores e atuadores possíveis de serem precadastrados
        query_result = session.query(TipoSensor.id_tipo_sensor).all()

        # Extrair os valores encontrados para uma lista de ids
        lista_ids_tipos_sensores_atuadores = [result[0] for result in query_result]

        return lista_ids_tipos_sensores_atuadores

    except SQLAlchemyError as e:
        return Exception(f"Erro ao obter lista de tipos de sensores e atuadores: {str(e)}")
    finally:
        session.close()

def precadastrar_sensor_atuador_base_dados(id_tipo_sensor):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Instanciar um model de sensor e atuaador, gerando um UUID na hora. A data será a corrente, gerada pelo próprio banco de dados
        sensor_atuador = SensorAtuador(
            uuid_sensor_atuador=str(uuid.uuid4()),
            id_tipo_sensor=id_tipo_sensor
        )

        # Fazer o commit das alterações no banco de dados
        session.add(sensor_atuador)
        session.commit()

        logging.info(f"[DAO - INFO] Sensor ou atuador precadastrado com sucesso. Gerado o uuid: {str(sensor_atuador.uuid_sensor_atuador)}")

        return sensor_atuador.uuid_sensor_atuador

    except SQLAlchemyError as e:
        session.rollback()

        return Exception(f"Erro ao precadastrar sensor ou atuador na base de dados: {str(e)}")
    finally:
        session.close()