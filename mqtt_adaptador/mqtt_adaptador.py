import paho.mqtt.client as mqtt


class MQTTAdapter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # MQTT client instance
            cls._instance.client = mqtt.Client()
            cls._instance.client.on_connect = cls._instance.on_connect
            cls._instance.client.on_message = cls._instance.on_message
            # Connect to the MQTT broker
            cls._instance.client.connect("18.214.223.254", 1883, 60)
            cls._instance.client.loop_start()
        return cls._instance

    def on_connect(self, client, userdata, flags, result_code):
        print("Conectado à instância MQTT com o código de resultado ", str(result_code))
        # Subscribe to the desired topics
        client.subscribe("planto-iot-sensores")

    def on_message(self, client, userdata, msg):
        print("Recebida mensagem via MQTT no tópico {" + msg.topic + "}: " + str(msg.payload))
        # Process the received message

    def publish(self, topic, payload):
        # Publish a message to the MQTT broker
        self.client.publish(topic, payload)

    def disconnect(self):
        # Disconnect from the MQTT broker
        self.client.loop_stop()
        self.client.disconnect()
