import os
from dotenv import load_dotenv

import paho.mqtt.client as mqtt
from kafka import KafkaProducer


class MQTTAdapter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Variáveis de ambiente

            # Carregar as variáveis de ambiente do arquivo .env
            load_dotenv()

            cls._instance.mqtt_host = os.environ.get('MQTT_HOST')
            cls._instance.mqtt_port = os.environ.get('MQTT_PORT')
            cls._instance.kafka_host = os.environ.get('KAFKA_HOST')
            cls._instance.kafka_port = os.environ.get('KAFKA_PORT')
            cls._instance.kafka_bootstrap_server_string = f"{cls._instance.kafka_host}:{cls._instance.kafka_port}"

            # Instância do cliente MQTT
            cls._instance.client = mqtt.Client()

            # Callbacks para o cliente MQTT
            cls._instance.client.on_connect = cls._instance.on_connect
            cls._instance.client.on_message = cls._instance.on_message

            # Conectar ao broker MQTT
            cls._instance.client.connect(cls._instance.mqtt_host, int(cls._instance.mqtt_port), 60)

            # Inscrever-se nos tópicos desejados
            cls._instance.client.subscribe("planto-iot-sensores/+/+/S")

            # Create Kafka producer instance
            cls._instance.producer = KafkaProducer(
                bootstrap_servers=cls._instance.kafka_bootstrap_server_string
            )

            # Inicia o cliente MQTT em loop (nova Thread)
            cls._instance.client.loop_start()
        return cls._instance

    def on_connect(self, client, userdata, flags, result_code):
        print("[ADAPTADOR MQTT - INFO] Conectado à instância MQTT com o código de resultado ", str(result_code))

    def on_message(self, client, userdata, msg):
        print("[ADAPTADOR MQTT - INFO]  Recebida mensagem via MQTT no tópico {" + msg.topic + "}: " + str(msg.payload))

        # Publicar a mensagem para um tópico do Apache Kafka - Relay de mensagens
        self.producer.send('planto-iot-sensores-kafka', str(msg.payload).encode('utf-8'))
        self.producer.flush()
        print(
            "[ADAPTADOR MQTT - INFO] Mensagem MQTT reencaminhada ao broker Kafka - Relay de mensagens - Tópico {planto-iot-sensores-kafka}")

    def publish(self, topic, payload):
        # Publish a message to the MQTT broker
        self.client.publish(topic, payload)
        print("[ADAPTADOR MQTT - INFO] Publicada mensagem ao broker MQTT no tópico {" + topic + "}: " + payload)

    def disconnect(self):
        # Disconnect from the MQTT broker
        self.client.loop_stop()
        self.client.disconnect()

        # Close the Kafka producer
        self.producer.flush()
        self.producer.close()
