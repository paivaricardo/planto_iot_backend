#!/usr/bin/python3
##!/usr/local/bin/python3.9
##!/usr/bin/python3

# Para executar dentro do PyCharm eh soh comentar a primeira linha acima

#
# Exemplo extraido de:
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

#
# Eh possivel fazer uma conexao TLS com o MQTT. Ver em:
# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

import random
import threading

from paho.mqtt import client as mqtt_client
from datetime import datetime

broker = '18.214.223.254'
#broker = 'mqtt.eclipseprojects.io'
#broker = 'iot.eclipse.org'
#broker = 'broker.emqx.io'
port = 1883
#port = 8883  # Porta segura TLS - requer certificado no cliente

PREFIX = "planto-iot-sensores"
topic_server_reading = f"{PREFIX}/+/+/S"
topic_client_reading = f"{PREFIX}/R"
# usuario e senha do topico .. pode ser em branco .. deve ser combinado entre o Pub/Sub
username = 'emqx'
password = 'public'
#username = ''
#password = ''

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


# Funcao de callback quando fizer a conexao ..
def callbackConexao(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker! My ID:", client_id)
        Subscribe(client)
    else:
        print("Failed to connect, return code %d\n", rc)


def callbackDesconexao(client, userdata, rc):
    print("Razao da desconexao: ", rc, sep='')
    print("Vou precisar reconectar ..")


def connect_mqtt() -> mqtt_client:
    print("Iniciando processo de conexao ..")
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = callbackConexao # Funcao de callback quando fizer a conexao ..
    client.on_disconnect = callbackDesconexao # Funcao de callback quando acontecer uma desconexao ..
    print("Conectando com o broker ", broker)
    # 'connect()' eh blocante???
    client.connect(broker, port)
    return client


# Funcao de callback quando chegar uma mensagem
def recebeMsg(client, userdata, msg):
    print(f"Recebi/li (RECEIVE) a mensagem `{msg.payload.decode()}` do topico `{msg.topic}`")

    # Se for necessario, posso enviar uma mensagem de volta para
    #   o cliente
    EnviaMsgParaCliente(client, msg)


def EnviaMsgParaCliente(client, origem):

    # Ainda nao vou enviar mensagens para o cliente ..
    return

    agora = datetime.now().strftime('%Y/%m/%d-%H:%M:%S.%f')[:-3]
    msg = f"{agora} messages: maquina de origem=SERVIDOR"
    # Respondendo aleatoriamente para fins de teste ..
    rand = random.randint(0, 4)
    if ( rand != 3 ):
        return

    list = origem.topic.split("/")
    FAZENDA_ORIGEM = list[2]
    AREA_ORIGEM = list[3]
    print(f"Enviando resposta para .. Fazenda: {FAZENDA_ORIGEM}; Area: {AREA_ORIGEM}")
    topico_resposta = f"{PREFIX}/{FAZENDA_ORIGEM}/{AREA_ORIGEM}/R"

    #result = client.publish(topic_client_reading, msg)
    result = client.publish(topico_resposta, msg)
    # result: [0, 1]
    status = result[0]
    print(f"Ret code: {status}-{result[1]}")
    if status == 0:
        print(f"Enviei (SEND) a mensagem `{msg}` para o topic `{topico_resposta}`")
    else:
        print(f"Falha ao enviar (SEND) mensagem para o topico {topico_resposta}. Retorno: {status}-{result[1]}")
    return


def Subscribe(client: mqtt_client):
    client.subscribe(topic_server_reading)
    print(f"Ativando funcao de callback de mensagens a receber .. topico: {topic_server_reading}")
    #
    # Como adicionar varias funcoes de callback para tratar mensagens:
    # https://stackoverflow.com/questions/41624697/mqtt-python-subscribe-to-multiple-topics-and-write-payloads-on-raspberry-lcd
    #
    client.on_message = recebeMsg # Funcao de callback quando chegar uma mensagem


def run():
    client = connect_mqtt()
    #Subscribe(client)

    # Ver: http://www.steves-internet-guide.com/loop-python-mqtt-client/
    # Agora fico bloqueado, aguardando chegar uma mensagem
    #   para ser acionado pela funcao de callback
    print("Entrando no loop eterno ..")
    client.loop_forever()


    print("SAINDO ??? do loop eterno ..")


#
# Codigo interessante de implememtar:
# https://groups.google.com/g/mqtt/c/H5kJ91Pr52g?pli=1
#

if __name__ == '__main__':
    jah_conectou_uma_vez = False

    run()
