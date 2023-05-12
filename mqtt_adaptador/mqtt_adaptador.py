import paho.mqtt.client as mqtt
from kafka import KafkaProducer

class MQTTAdapter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Instância do cliente MQTT
            cls._instance.client = mqtt.Client()

            # Callbacks para o cliente MQTT
            cls._instance.client.on_connect = cls._instance.on_connect
            cls._instance.client.on_message = cls._instance.on_message

            # Conectar ao broker MQTT
            cls._instance.client.connect("18.214.223.254", 1883, 60)

            # Inscrever-se nos tópicos desejados
            cls._instance.client.subscribe("planto-iot-sensores/+/+/S")

            # Create Kafka producer instance
            cls._instance.producer = KafkaProducer(bootstrap_servers='18.214.223.254:9092')

            # Inicia o cliente MQTT em loop
            cls._instance.client.loop_start()
        return cls._instance

    def on_connect(self, client, userdata, flags, result_code):
        print("Conectado à instância MQTT com o código de resultado ", str(result_code))

    def on_message(self, client, userdata, msg):
        print("Recebida mensagem via MQTT no tópico {" + msg.topic + "}: " + str(msg.payload))

        # Publicar a mensagem para um tópico do Apache Kafka - Relay de mensagens
        self.producer.send('planto-iot-sensores-kafka', msg.payload)

        print("Enviada a mensagem do broker Kafka")


    def publish(self, topic, payload):
        # Publish a message to the MQTT broker
        self.client.publish(topic, payload)

    def disconnect(self):
        # Disconnect from the MQTT broker
        self.client.loop_stop()
        self.client.disconnect()

        # Close the Kafka producer
        self.producer.close()
