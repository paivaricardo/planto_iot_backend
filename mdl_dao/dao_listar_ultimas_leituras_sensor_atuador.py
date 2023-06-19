import logging
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.leitura_atuacao_model import LeituraAtuacao
from model.sensor_atuador_model import SensorAtuador


def listar_ultimas_leituras_sensor_atuador_servico(uuid_sensor_atuador: UUID, num_ultimas_leituras: int, filtragem_tipo_sinal: int):
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