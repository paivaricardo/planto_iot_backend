import datetime
import json
import logging
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.leitura_atuacao_model import LeituraAtuacao
from model.sensor_atuador_model import SensorAtuador


def listar_ultimas_leituras_sensor_atuador_servico(uuid_sensor_atuador: UUID, num_ultimas_leituras: int,
                                                   filtragem_tipo_sinal: int):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:
        query = None

        # Buscar a lista as x últimas leituras do sensor com o uuid informado
        if filtragem_tipo_sinal == 0:
            # Buscar as x últimas leituras do sensor/atuador de uuid informado
            query = session.query(LeituraAtuacao). \
                join(SensorAtuador). \
                filter(SensorAtuador.uuid_sensor_atuador == str(uuid_sensor_atuador)). \
                order_by(desc(LeituraAtuacao.data_hora_leitura)). \
                limit(num_ultimas_leituras)
        else:
            query = session.query(LeituraAtuacao). \
                join(SensorAtuador). \
                filter(SensorAtuador.uuid_sensor_atuador == str(uuid_sensor_atuador)). \
                filter(LeituraAtuacao.id_tipo_sinal == filtragem_tipo_sinal). \
                order_by(desc(LeituraAtuacao.data_hora_leitura)). \
                limit(num_ultimas_leituras)

        # Executar a query
        lista_leituras_result = query.all()

        return lista_leituras_result

    except SQLAlchemyError as e:
        logging.error(
            f"[DAO - ERRO] Erro ao tentar obter as últimas {num_ultimas_leituras} do sensor/atuador de UUID {uuid_sensor_atuador}: {str(e)}")
        raise Exception(
            f"[DAO - ERRO] Erro ao tentar obter as últimas {num_ultimas_leituras} do sensor/atuador de UUID {uuid_sensor_atuador}: {str(e)}")
    finally:
        session.close()


def listar_leituras_sensor_atuador_por_data(uuid_sensor_atuador: UUID, begin_date_timestamp: datetime.datetime,
                                            end_date_timestamp: datetime.datetime, filtragem_tipo_sinal: int, simplificado: bool = False):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:
        query = session.query(LeituraAtuacao). \
            join(SensorAtuador). \
            filter(SensorAtuador.uuid_sensor_atuador == str(uuid_sensor_atuador)). \
            filter(LeituraAtuacao.id_tipo_sinal == filtragem_tipo_sinal). \
            filter(LeituraAtuacao.data_hora_leitura >= begin_date_timestamp). \
            filter(LeituraAtuacao.data_hora_leitura <= end_date_timestamp). \
            order_by(desc(LeituraAtuacao.data_hora_leitura))

        # Executar a query
        lista_leituras_result = query.all()

        if simplificado:
            lista_leituras_result_dicts = [{
                "data_hora_leitura": leitura.data_hora_leitura,
                "json_leitura": json.loads(leitura.json_leitura),
            } for leitura in lista_leituras_result]
        else:
            lista_leituras_result_dicts = [{
                "id_leitura_atuacao": leitura.id_leitura_atuacao,
                "data_hora_leitura": leitura.data_hora_leitura,
                "json_leitura": json.loads(leitura.json_leitura),
                "id_sensor_atuador": leitura.id_sensor_atuador,
                "id_tipo_sinal": leitura.id_tipo_sinal,
            } for leitura in lista_leituras_result]

        return lista_leituras_result_dicts

    except SQLAlchemyError as e:
        logging.error(
            f"[DAO - ERRO] Erro ao tentar obter as leituras do sensor/atuador de UUID {uuid_sensor_atuador} entre {begin_date_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')} e {end_date_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')}: {str(e)}")
        raise Exception(
            f"[DAO - ERRO] Erro ao tentar obter as leituras do sensor/atuador de UUID {uuid_sensor_atuador} entre {begin_date_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')} e {end_date_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')}: {str(e)}")
    finally:
        session.close()
