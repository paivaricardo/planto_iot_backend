import logging
import threading
import os

import uvicorn
from dotenv import load_dotenv

from mdl_proc_mensagens.processamento_mensagens import processamento_mensagens_kafka_consumer_thread
from mdl_rest_api.rest_api_core import app
from mqtt_adaptador.mqtt_adaptador import MQTTAdapter

if __name__ == '__main__':
    # Definir nível de log
    logging.basicConfig(filename="application.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Carregar as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Criar uma thread para o processamento de mensagens oriundas do broker Kafka
    processamento_mensagens_thread = threading.Thread(target=processamento_mensagens_kafka_consumer_thread)

    # Start the Kafka consumer thread
    processamento_mensagens_thread.start()

    # Criar uma instância do adaptador MQTT
    mqtt_adapter = MQTTAdapter()

    # Colocar a instância do adaptador MQTT numa thread própria
    # mqtt_adapter_thread = threading.Thread(target=mqtt_adapter)

    # Start the MQTT Adapter thread
    # mqtt_adapter_thread.start()

    # Rodar a REST API implementada com a FastAPI em uma thread própria, com utilização da biblioteca uvicorn
    def run_fastapi():
        logging.info("Iniciando o servidor FastAPI...")
        uvicorn.run(app, host=os.environ.get("FAST_API_HOST"), port=int(os.environ.get("FAST_API_PORT")))

    # Criar uma thread própria para a REST API em FastAPI e iniciar
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()

    logging.info("REST API com a FastAPI inicializada com sucesso!")

    # Terminar as threads conjuntamente
    # mqtt_adapter_thread.join()
    processamento_mensagens_thread.join()
    fastapi_thread.join()

