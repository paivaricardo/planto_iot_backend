import logging
import uuid
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.sensor_atuador_model import SensorAtuador
from model.tipo_sensor_model import TipoSensor


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


def precadastrar_sensor_atuador_base_dados(id_tipo_sensor, uuid_selecionado: Optional[uuid.UUID] = None):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Instanciar um model de sensor e atuaador, gerando um UUID na hora. A data será a corrente, gerada pelo próprio banco de dados
        sensor_atuador = SensorAtuador(
            uuid_sensor_atuador=str(uuid_selecionado) if uuid_selecionado is not None else str(uuid.uuid4()),
            id_tipo_sensor=id_tipo_sensor
        )

        # Buscar o nome do tipo de sensor ou atuador
        tipo_sensor = session.query(TipoSensor).filter_by(id_tipo_sensor=id_tipo_sensor).first()

        # Fazer o commit das alterações no banco de dados
        session.add(sensor_atuador)
        session.commit()

        sensor_atuador_precadastrado_dict = {
            "id_sensor_atuador": sensor_atuador.id_sensor_atuador,
            "uuid_sensor_atuador": sensor_atuador.uuid_sensor_atuador,
            "data_precadastro_sensor": sensor_atuador.data_precadastro_sensor.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            "id_tipo_sensor": sensor_atuador.id_tipo_sensor,
            "nome_tipo_sensor": tipo_sensor.nome_tipo_sensor,
        }

        logging.info(
            f"[DAO - INFO] Sensor ou atuador precadastrado com sucesso. Gerado o uuid: {str(sensor_atuador.uuid_sensor_atuador)}")

        return sensor_atuador_precadastrado_dict

    except SQLAlchemyError as e:
        session.rollback()

        return Exception(f"Erro ao precadastrar sensor ou atuador na base de dados: {str(e)}")
    finally:
        session.close()


def verificar_uuid_selecionado_inedito(uuid_selecionado: uuid.UUID):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:
        sensor_atuador = session.query(SensorAtuador).filter_by(uuid_sensor_atuador=str(uuid_selecionado)).first()

        if sensor_atuador is None:
            logging.info(f"[DAO - INFO] UUID selecionado {uuid_selecionado} é inédito na base de dados.")
            return True
        else:
            logging.info(f"[DAO - INFO] UUID selecionado {uuid_selecionado} já está cadastrado na base de dados.")
            return False

    except SQLAlchemyError as e:
        return Exception(f"Erro ao verificar se o uuid selecionado é inédito: {str(e)}")
    finally:
        session.close()
