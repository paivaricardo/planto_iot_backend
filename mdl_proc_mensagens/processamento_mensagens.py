from kafka import KafkaConsumer
from kafka.errors import KafkaError


def processar_mensagem(message):
    # Process the message here
    print("Recebida a mensagem do broker kafka:", message)


def processamento_mensagens_kafka_consumer_thread():
    print("Iniciado o módulo de processamento de mensagens.")

    consumer = KafkaConsumer(
        "planto-iot-sensores-kafka",
        bootstrap_servers="18.214.223.254:9092"
    )

    try:
        for mensagem in consumer:
            processar_mensagem(mensagem.value.decode("utf-8"))
    except KafkaError as e:
        print("Kafka Error:", e)
    finally:
        consumer.close()
