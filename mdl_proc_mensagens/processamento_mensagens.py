import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import re
from mdl_validador_mensagens import validacao_mensagens
from mdl_dao import dao_mensagens_sensores_atuadores

def processar_mensagem(message, topic):
    logging.info("[PROC MENSAGENS - INFO] Iniciado o processamento da mensagem.")

    # Carregar as variáveis de ambiente do arquivo .env
    load_dotenv()

    try:
        # Decodificar a mensagem em json para um dicionário Python:
        print("[PROC MENSAGENS - INFO] Mensagem recebida:", message)
        json_raw_message = re.sub(r"^b'|'$", "", message)
        mensagem_dict = json.loads(json_raw_message)

        # Converter a data-hora da mensagem para o formato datetime de Python
        mensagem_dict["dataHoraAcionamentoLeitura"] = datetime.strptime(mensagem_dict["dataHoraAcionamentoLeitura"], "%Y-%m-%dT%H:%M:%S.%f%z")

        logging.info("[PROC MENSAGENS - INFO] Mensagem decodificada em dicionário Python:", mensagem_dict)

        # Executar validações da mensagem
        logging.info("[PROC MENSAGENS - INFO] Iniciando validações da mensagem.")
        # Validação inicial de uuid do sensor
        if not validacao_mensagens.validar_uuid_sensor_atuador(mensagem_dict):
            raise Exception("Mensagem descartada devido a inconsistência de uuid do sensor.")

        # Validação da consistência de atributos do sensor
        if not validacao_mensagens.validar_consistencia_atributos_sensor(mensagem_dict):
            raise Exception("Mensagem descartada devido a inconsistência de atributos do sensor.")

        # Validação da consistência de atributos do sensor
        if not validacao_mensagens.validar_consistencia_dados_sensor(mensagem_dict):
            raise Exception("Mensagem descartada devido a inconsistência de dados do sensor.")

        logging.info("[PROC MENSAGENS - INFO] Mensagem validada.")

        # Gravar a mensagem no banco de dados
        logging.info("[PROC MENSAGENS - INFO] Iniciando gravação da mensagem no banco de dados.")

        # De acordo com o tipo de sinal, chamar diferentes funções do DAO para persistir na base de dados
        if mensagem_dict["tipoSinal"] == 10000:
            logging.info("[PROC MENSAGENS - INFO] Redirecionando a mensagem de LEITURA DE SENSORES para o módulo de persistência do DAO.")
            dao_mensagens_sensores_atuadores.persistir_leitura_sensor_atuador(mensagem_dict)

        if mensagem_dict["tipoSinal"] == 50001:
            logging.info("[PROC MENSAGENS - INFO] Redirecionando a mensagem de ACK DE ACIONAMENTO DE ATUADORES para o módulo de persistência do DAO.")
            dao_mensagens_sensores_atuadores.persistir_ack_atuador(mensagem_dict)

    except Exception as e:
        logging.info("[PROC MENSAGENS - ERRO] Erro no processamento da mensagem", e.args[0])
        return

def processamento_mensagens_kafka_consumer_thread():
    logging.info("[PROC MENSAGENS - INFO] Iniciado o módulo de processamento de mensagens do Planto-IoT Backend.")
    topic = "planto-iot-sensores-kafka"

    # Instanciar um consumidor Kafka para receber mensagens oriundas do broker Kafka, após relay de mensagens do MQTT
    consumer = KafkaConsumer(
        "planto-iot-sensores-kafka",
        bootstrap_servers=f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"
    )

    # Assim que o consumidor Kafka receber uma mensagem, enviar para processamento
    try:
        for message in consumer:
            print("[PROC MENSAGENS - INFO] Recebida a mensagem do broker Kafka no tópico:", topic, "mensagem:", message.value.decode("utf-8"))
            processar_mensagem(message.value.decode("utf-8"), topic)
    except KafkaError as e:
        logging.info("[PROC MENSAGENS - ERRO] Kafka Error:", e)
    finally:
        consumer.close()
