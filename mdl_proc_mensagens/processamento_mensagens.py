from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import re
from mdl_validador_mensagens import validacao_mensagens

def processar_mensagem(message, topic):
    #
    print("[PROC MENSAGENS - INFO] Iniciado o processamento da mensagem.")
    try:
        # Decodificar a mensagem em json para um dicionário Python:
        print("[PROC MENSAGENS - INFO] Mensagem recebida:", message)
        json_raw_message = re.sub(r"^b'|'$", "", message)
        mensagem_dict = json.loads(json_raw_message)
        print("[PROC MENSAGENS - INFO] Mensagem decodificada em dicionário Python:", mensagem_dict)

        # Executar validações da mensagem
        print("[PROC MENSAGENS - INFO] Iniciando validações da mensagem.")
        # Validação inicial de uuid do sensor
        if not validacao_mensagens.validar_uuid_sensor_atuador(mensagem_dict):
            raise Exception("Mensagem descartada devido a inconsistência de uuid do sensor.")

        # Validação da consistência de atributos do sensor
        if not validacao_mensagens.validar_consistencia_atributos_sensor(mensagem_dict):
            raise Exception("Mensagem descartada devido a inconsistência de atributos do sensor.")

        # Validação da consistência de atributos do sensor
        if not validacao_mensagens.validar_consistencia_dados_sensor(mensagem_dict):
            raise Exception("Mensagem descartada devido a inconsistência de dados do sensor.")

        print("[PROC MENSAGENS - INFO] Mensagem validada.")

        # Gravar a mensagem no banco de dados
        print("[PROC MENSAGENS - INFO] Iniciando gravação da mensagem no banco de dados.")
        

    except Exception as e:
        print("[PROC MENSAGENS - ERRO] Erro no processamento da mensagem", e.args[0])
        return

def processamento_mensagens_kafka_consumer_thread():
    print("[PROC MENSAGENS - INFO] Iniciado o módulo de processamento de mensagens do Planto-IoT Backend.")
    topic = "planto-iot-sensores-kafka"

    # Instanciar um consumidor Kafka para receber mensagens oriundas do broker Kafka, após relay de mensagens do MQTT
    consumer = KafkaConsumer(
        "planto-iot-sensores-kafka",
        bootstrap_servers="18.214.223.254:9092"
    )

    # Assim que o consumidor Kafka receber uma mensagem, enviar para processamento
    try:
        for message in consumer:
            print("[PROC MENSAGENS - INFO] Recebida a mensagem do broker Kafka no tópico:", topic, "mensagem:", message.value.decode("utf-8"))
            processar_mensagem(message.value.decode("utf-8"), topic)
    except KafkaError as e:
        print("[PROC MENSAGENS - ERRO] Kafka Error:", e)
    finally:
        consumer.close()
