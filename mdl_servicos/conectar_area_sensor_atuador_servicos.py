from mdl_interacao_sensores_atuadores.interacao_geral_sensores_atuadores import \
    enviar_informacao_conexao_area_sensor_atuador
from model.query_models.sensor_atuador_query_model import SensorAtuadorQueryModel


def conectar_area_sensor_atuador_servico(sensor_atuador_query_model_dict: SensorAtuadorQueryModel):
    """Aciona o módulo de interação com sensores e atuadores para conectar o sensor ou atuador à área. Informação relevante apenas para os sensores/atuadores virtualizados"""
    return enviar_informacao_conexao_area_sensor_atuador(sensor_atuador_query_model_dict)
