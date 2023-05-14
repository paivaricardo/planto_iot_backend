import threading

from mdl_proc_mensagens.processamento_mensagens import processamento_mensagens_kafka_consumer_thread
from mqtt_adaptador.mqtt_adaptador import MQTTAdapter

if __name__ == '__main__':

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

    # Terminar as threads conjuntamente
    # mqtt_adapter_thread.join()
    processamento_mensagens_thread.join()

