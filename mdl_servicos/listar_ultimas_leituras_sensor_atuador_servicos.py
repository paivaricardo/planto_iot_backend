import json
from uuid import UUID

from mdl_dao import dao_listar_ultimas_leituras_sensor_atuador


def listar_ultimas_leituras_sensor_atuador_servico(uuid_sensor_atuador: UUID, num_ultimas_leituras: int,
                                                   filtragem_tipo_sinal: int):
    try:
        lista_leituras =  dao_listar_ultimas_leituras_sensor_atuador.listar_ultimas_leituras_sensor_atuador_servico(
            uuid_sensor_atuador, num_ultimas_leituras, filtragem_tipo_sinal)

        # Transformar os campos "json_leitura", que estava codificado com uma String no banco de dados, em um objeto JSON
        for leitura in lista_leituras:
            leitura.json_leitura = json.loads(leitura.json_leitura)

        return lista_leituras

    except Exception as e:
        raise Exception(
            f"[SERVIÇO - ERRO] Erro ao tentar obter as últimas {num_ultimas_leituras} do sensor/atuador de UUID {uuid_sensor_atuador}: {str(e)}")
