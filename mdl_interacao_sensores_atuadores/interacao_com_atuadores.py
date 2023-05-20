import datetime
import json

from mqtt_adaptador.mqtt_adaptador import MQTTAdapter


def enviar_sinal_atuador(uuid_atuador: str, quantidade_atuacao: int):
    """
    Envia um sinal para ativação de um atuador específico no Planto IoT.
    """
    try:
        topico_ativacao_atuacao = f"planto-iot-sensores/atuadores/{uuid_atuador}/A"
        payload_mensagem_ativacao_atuacao = {
            "uuidSensorAtuador": uuid_atuador,
            "dataHoraAcionamentoLeitura": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            "tipoSinal": 50000,
            "quantidadeAtuacao": quantidade_atuacao
        }

        # Instanciar o adaptador MQTT (instância singleton do adaptador MQTT)
        mqtt_adapter = MQTTAdapter()

        mqtt_adapter.publish(topico_ativacao_atuacao, json.dumps(payload_mensagem_ativacao_atuacao))

        return True
    except Exception as e:
        raise Exception("Erro ao ativar o atuador", str(e))