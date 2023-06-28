from datetime import datetime
from uuid import UUID

from mdl_dao import dao_listar_ultimas_leituras_sensor_atuador, dao_verificar_sensor_atuador
from mdl_reports import report_leituras_sensor_atuador_grafico


def gerar_relatorio_leitura_sensor_servico(uuid_sensor: UUID, begin_date_timestamp: datetime, end_date_timestamp: datetime, filtragem_tipo_sinal: int):
    try:
        informacoes_sensor = dao_verificar_sensor_atuador.verificar_existencia_sensor_atuador_base_dados(uuid_sensor)

        if not informacoes_sensor["sensor_atuador_existe_bd"] or not informacoes_sensor["sensor_atuador_foi_cadastrado"]:
            raise Exception(f"[SERVICO - RELATORIOS - ERRO] O sensor de UUID {uuid_sensor} não existe ou não foi "
                            f"cadastrado no banco de dados.")

        leituras_sensor_dicts = dao_listar_ultimas_leituras_sensor_atuador.listar_leituras_sensor_atuador_por_data(uuid_sensor, begin_date_timestamp, end_date_timestamp, filtragem_tipo_sinal)

        if len(leituras_sensor_dicts) == 0:
            return None

        relatorio_image_encoded = report_leituras_sensor_atuador_grafico.gerar_relatorio_leitura_sensor(informacoes_sensor, leituras_sensor_dicts)

        return relatorio_image_encoded
    except Exception as e:
        raise Exception(f"[SERVICO - ERRO] Erro ao tentar gerar o relatório de leitura do sensor: {str(e)}")


def obter_relatorio_leituras_sensor_servico(uuid_sensor, begin_date_timestamp, end_date_timestamp,
                                            filtragem_tipo_sinal):
    try:
        informacoes_sensor = dao_verificar_sensor_atuador.verificar_existencia_sensor_atuador_base_dados(uuid_sensor)

        if not informacoes_sensor["sensor_atuador_existe_bd"] or not informacoes_sensor[
            "sensor_atuador_foi_cadastrado"]:
            raise Exception(f"[SERVICO - RELATORIOS - ERRO] O sensor de UUID {uuid_sensor} não existe ou não foi "
                            f"cadastrado no banco de dados.")

        leituras_sensor_dicts = dao_listar_ultimas_leituras_sensor_atuador.listar_leituras_sensor_atuador_por_data(
            uuid_sensor, begin_date_timestamp, end_date_timestamp, filtragem_tipo_sinal)

        if len(leituras_sensor_dicts) == 0:
            return None

        return leituras_sensor_dicts
    except Exception as e:
        raise Exception(f"[SERVICO - ERRO] Erro ao tentar obter as leituras do sensor para relatório: {str(e)}")