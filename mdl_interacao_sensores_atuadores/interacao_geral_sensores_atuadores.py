import datetime
import json
import logging

from model.pydantic_rest_models.sensor_atuador_cadastro_completo_rest_model import SensorAtuadorCadastroCompleto
from mqtt_adaptador.mqtt_adaptador import MQTTAdapter


def enviar_informacao_conexao_area_sensor_atuador(sensor_atuador_cadastro_completo: SensorAtuadorCadastroCompleto):
    """
    Envia informação de área do sensor/atuador para o broker MQTT, que servirá para a conexão dos sensores e atuadores virtualizados a determinada área, indicada pelo id da área.
    """
    try:
        topico_info_conexao_area = f"planto-iot-sensores/{sensor_atuador_cadastro_completo.uuid_sensor_atuador}"

        payload_mensagem_conexao_area = {
            "uuidSensorAtuador": str(sensor_atuador_cadastro_completo.uuid_sensor_atuador),
            "dataHoraConexaoArea": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            "tipoSinal": 60100,
            "idAreaConectada": sensor_atuador_cadastro_completo.id_area,
        }

        # Instanciar o adaptador MQTT (instância singleton do adaptador MQTT)
        mqtt_adapter = MQTTAdapter()

        # Publicar a mensagem de ativação do atuador no tópico, direcionada ao broker MQTT
        mqtt_adapter.publish(topico_info_conexao_area, json.dumps(payload_mensagem_conexao_area))

        logging.info(
            f"[INTER. ATUADORES - INFO] Enviado sinal de conexão com a área {sensor_atuador_cadastro_completo.id_area} para o sensor/atuador de UUID {sensor_atuador_cadastro_completo.uuid_sensor_atuador} com sucesso!")

        return True
    except Exception as e:
        logging.error(f"Erro enviar mensagem de conexão com a área: {str(e)}")
        return False
