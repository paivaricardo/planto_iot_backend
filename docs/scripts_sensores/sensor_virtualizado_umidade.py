#!/usr/bin/python3
##!/usr/local/bin/python3.9
##!/usr/bin/python3.9

# Para executar dentro do PyCharm eh soh comentar a primeira linha acima

#
# Exemplo extraido de:
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

'''
ESPECIFICACOES do sensor de umidade do solo modelo SMTHS07
Extraido de:
https://smartec-sensors.eu/cms/media/Datasheets/Humidity/HUMIDITY_datasheet.pdf
Temperatuda de operacao: -40~120 Celsius
Sensitividade tipica: 0,6
Capacitancia aa 55% de umidade (Cs): 350 pF
Calculo da umidade: Xrh = (Cc - Cs)/S + 55
	onde:
	Cc = capacitancia medida
	Cs = Capacitancia aa 55% de umidade
	S  = Sensitividade
Range de operacao de umidade: 0~100%
'''

import random
import time
import os
import ctypes
import threading
import argparse

from paho.mqtt import client as mqtt_client
from datetime import datetime

BROKER = '18.214.223.254'
# BROKER = 'mqtt.eclipseprojects.io'
# BROKER = 'iot.eclipse.org'
# BROKER = 'broker.emqx.io'
PORTA = 1883
# PORTA = 8883  # Porta segura TLS - requer certificado no cliente
#
# Eh possivel fazer uma conexao TLS com o MQTT. Ver em:
# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php


MIN_CAP = 317  # 0% umidade
MAX_CAP = 377  # 100% umidade

MAX_UMID = 100
MIN_UMID = 0

DESCRICAO_SENSOR = "SMTHS07"

# Hierarquia:
# Fazenda/Area
FAZENDA = "Fazenda00"
AREA = "Area51"

FAZENDA = ""
AREA = ""

TOPICO_RAIZ = "planto-iot-sensores"
# usuario e senha do topico .. pode ser em branco .. deve ser combinado entre o Pub/Sub
username = 'emqx'
password = 'public'
# username = ''
# password = ''

TOPIC_CLIENT_SENDING = ""
TOPIC_CLIENT_READING = ""

# Tempo hipotetico de amostragem para efeitos de testes - em segundos
# (aceita 0.3 segundos, por exemplo)
TEMPO_AMOSTRAGEM = 7.01

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def Usage():
    global TEMPO_AMOSTRAGEM
    global FAZENDA
    global AREA

    # Extraido de:
    # https://pythonhelp.wordpress.com/2011/11/20/tratando-argumentos-com-argparse/

    parser = argparse.ArgumentParser(description='Um simulador de sensor de UMIDADE. \
        Simular diversos sensores para uma determinada fazenda+area. \
        As fazendas e as respectivas areas dela, devem obedecer uma hierarquia MQTT, \
        tal como: topico_raiz/fazenda/area, onde "topico_raiz" estah hard-coded aqui. \
        "fazenda" e "area" sao valores obrigatorios que devem ser passados como argumento. \
        Uma mesma "fazenda" pode ter varias "areas" onde ficam os diversos sensores. \
        ')
    #    Indormar a fazenda (obrigatorio)
    parser.add_argument('--farm', action='store', dest='farm',
                        default="Fazenda00", type=ascii, required=False,
                        help='nome da fazenda, numa hierarquia MQTT: topico_raiz/fazenda/area')
    parser.add_argument('--area', action='store', dest='area',
                        default="Area51", type=ascii, required=False,
                        help='nome da area da fazenda onde estah o sensor')
    parser.add_argument('--timesample', action='store', dest='timesample',
                        default=TEMPO_AMOSTRAGEM, type=float, required=False,
                        help=f'de quanto tempo em quanto tempo, em segundos (pode ser fracao de segundo), o sensor farah a leitura da umidade e a enviarah (valor default: {TEMPO_AMOSTRAGEM}).')

    # verificacao de argumentos
    # Se tiver erro, o programa eh encerrado aqui mesmo ..
    args = parser.parse_args()

    print(f"Topico MQTT: {args.farm}/{args.area} ")
    print("Tempo da amostragem: ", args.timesample, sep='')

    return args


def SetGlobal(args):
    global TEMPO_AMOSTRAGEM
    global TOPICO_RAIZ
    global FAZENDA
    global AREA
    global TOPIC_CLIENT_SENDING
    global TOPIC_CLIENT_READING

    if (args.timesample >= 0.0):
        TEMPO_AMOSTRAGEM = args.timesample

    FAZENDA = args.farm
    AREA = args.area

    print(args.farm)
    print(args.area)
    print(args.timesample)

    TOPIC_CLIENT_SENDING = f"{TOPICO_RAIZ}/{FAZENDA}/{AREA}/S"
    TOPIC_CLIENT_READING = f"{TOPICO_RAIZ}/{FAZENDA}/{AREA}/R"
    print("Topico escrita: ", TOPIC_CLIENT_SENDING)
    print("Topico leitura: ", TOPIC_CLIENT_READING)

    return 0


# Funcao de callback quando fizer a conexao ..
def callbackConexao(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker! My ID:", client_id)
    else:
        print("Failed to connect, return code %d\n", rc)


def connect_mqtt():
    print("Cliente: -> Entrando na funcao connect_mqtt() ..")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = callbackConexao  # Funcao de callback quando fizer a conexao ..
    # 'connect()' eh blocante???
    client.connect(BROKER, PORTA)

    print("Cliente: <- Saindo da funcao connect_mqtt() ..")
    return client


def Publish(client):
    print("Cliente: -> Entrando na funcao Publish() ..")

    msg_count = 0
    # Se nao ficar em loop (while(true)),
    #   somente 'msg_count' mensagens serao enviadas

    # while (msg_count < 10):
    while True:
        # time.sleep(7.01)
        time.sleep(TEMPO_AMOSTRAGEM)

        msg = MontarMensagem()

        result = client.publish(TOPIC_CLIENT_SENDING, msg)
        # result: [0, 1]
        status = result[0]
        print(f"Ret code: {status}-{result[1]}")
        if status == 0:
            print(f"Enviei (SEND) a mensagem `{msg}` para o topic `{TOPIC_CLIENT_SENDING}`")
        else:
            print(
                f"Falha ao enviar (SEND) mensagem para o topico {TOPIC_CLIENT_SENDING}. Retorno: {status}-{result[1]}")
        msg_count += 1

    print("Cliente: <- Saindo da funcao Publish() ..")


def MontarMensagem():
    msg = "{"

    uuid_sensor = ExtraiUUID()
    msg += f" \"uuidSensorAtuador\": \"{uuid_sensor}\","

    hora_agora = ExtraiHora()
    msg += f" \"dataHoraAcionamentoLeitura\": \"{hora_agora}\","

    tipo_sinal = 10000
    msg += f" \"tipoSinal\": {tipo_sinal},"

    msg += f" \"informacoesEspecificasSensor\": "
    msg += "{"

    umidade = MedeUmidade()
    msg += f" \"percentualUmidadeSolo\": \"{umidade}\" "

    msg += "} "
    msg += "}"

    return msg


def ExtraiUUID():
    # Fazer a geracao de UUID's distintos, por sensor ..
    return "b97b7ac5-7167-4a31-b4b8-b67c987ddf5b"


def ExtraiHora():
    # Fazer a formatacao correta ...
    # agora = datetime.now().strftime('%Y/%m/%d-%H:%M:%S.%f')[:-3]
    agora = "Friday, May 12, 2023 6:07:37 PM GMT-03:00"
    return agora


def MedeUmidade():
    # vamos gerar uma umidade randomica .. para testes ..
    # o correto serah capturar o teclado e verificar o que o usuairo estah digitando (poderia capturar as setas):
    # + aumenta a umidade
    # - diminui a umidade
    # umid_medida = random.randint(58, 80)

    # O calculo poderia ser com a capacitancia ..
    CS = 350
    S = 0.6
    CC = random.randint(MIN_CAP, MAX_CAP)
    umid_medida = '{0:.2f}'.format(((CC - CS) / S) + 55)  # 2 casas decimais

    return umid_medida

    # tmp = f'{MIN_UMID};{umid_medida};{MAX_UMID}'
    # return tmp


# def Subscribe(client: mqtt_client):
def Subscribe(client):
    print("Cliente: -> Entrando na funcao Subscribe() ..")
    client.subscribe(TOPIC_CLIENT_READING)
    print("Ativando funcao de callback de mensagens a receber .. topico: ", TOPIC_CLIENT_READING)

    # Subscrevendo a varios sub-topicos:
    # https://medium.com/analytics-vidhya/short-introduction-to-mqtt-with-python-e625c337c8f5
    #
    # OU
    #
    # Como adicionar varias funcoes de callback para tratar mensagens:
    # https://stackoverflow.com/questions/41624697/mqtt-python-subscribe-to-multiple-topics-and-write-payloads-on-raspberry-lcd
    #
    client.on_message = recebeMsg  # Funcao de callback quando chegar uma mensagem
    print("Cliente: <- Saindo da funcao Subscribe() ..")


# Funcao de callback quando chegar uma mensagem
def recebeMsg(client, userdata, msg):
    print(f"Recebi/li (RECEIVE) a mensagem `{msg.payload.decode()}` do  topico `{msg.topic}`")


#
# Codigo interessante de implememtar:
# https://groups.google.com/g/mqtt/c/H5kJ91Pr52g?pli=1
#

if __name__ == '__main__':
    # Recebendo parametros da linha de comando (like getopt())
    args = Usage()
    SetGlobal(args)

    print("Cliente: -> Entrando na funcao main() ..")

    client = connect_mqtt()

    # Vou me subscrever, *APESAR* de ser um sensor, para receber
    # mensagens de alerta do servidor central, caso ele as emita ..
    # Nao eh obrigatoria a subscricao .. eh como vamos/poderemos funcionar ..
    Subscribe(client)

    # python 3.8+ para buscar a TID
    print(threading.get_native_id())

    # loop_start() cria uma thread .. ??
    client.loop_start()

    # python 3.8+ para buscar a TID
    print(threading.get_native_id())

    Publish(client)
    client.loop_stop()

    print("Cliente: <- Saindo da funcao main() ..")