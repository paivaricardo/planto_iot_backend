import json
import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.sensor_atuador_model import SensorAtuador
from model.leitura_atuacao_model import LeituraAtuacao


def persistir_leitura_sensor_atuador(mensagem_dict):
    try:

        # Criar uma sessão para acesso ao banco de dados
        session = database.create_session()

        # Buscar id do sensor atuador no banco de dados, gravar na variável sensor_atuador
        sensor_atuador = session.query(SensorAtuador).filter(SensorAtuador.uuid_sensor_atuador == mensagem_dict['uuidSensorAtuador']).first()

        if not sensor_atuador:
            print("[DAO - ERRO] Sensor não encontrado no banco de dados.")
            raise ValueError("Sensor não encontrado no banco de dados.")

        # Criar uma nova instância do modelo LeituraAtuacao
        leitura_atuacao = LeituraAtuacao(
            data_hora_leitura=mensagem_dict['dataHoraAcionamentoLeitura'],
            json_leitura=json.dumps(mensagem_dict['informacoesEspecificasSensor']),
            id_sensor_atuador=sensor_atuador.id_sensor_atuador,  # Set the appropriate sensor ID
            id_tipo_sinal=mensagem_dict['tipoSinal']
        )

        # Persist the LeituraAtuacao object in the database
        session.add(leitura_atuacao)
        session.commit()

        logging.info(f"[DAO - INFO] Leitura persistida com sucesso. Gerado o id: {leitura_atuacao.id_leitura_atuacao}")

        return leitura_atuacao.id_leitura_atuacao  # Return the generated ID if needed

    except SQLAlchemyError as e:
        session.rollback()
        # Handle the exception as needed
        print(f"Error occurred while persisting sensor reading: {str(e)}")

    finally:
        session.close()

    return None


def persistir_ack_atuador(mensagem_dict):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Buscar id do sensor atuador no banco de dados, gravar na variável sensor_atuador
        sensor_atuador = session.query(SensorAtuador).filter(SensorAtuador.uuid_sensor_atuador == mensagem_dict['uuidSensorAtuador']).first()

        # Criar uma nova instância do modelo LeituraAtuacao
        leitura_atuacao = LeituraAtuacao(
            data_hora_leitura=mensagem_dict['dataHoraAcionamentoLeitura'],
            json_leitura=json.dumps({"mensagem": "ACK"}),
            id_sensor_atuador=sensor_atuador.id_sensor_atuador,  # Set the appropriate sensor ID
            id_tipo_sinal=mensagem_dict['tipoSinal']
        )

        # Persist the LeituraAtuacao object in the database
        session.add(leitura_atuacao)
        session.commit()

        logging.info(f"[DAO - INFO] Ack de acionamento do atuador persistido com sucesso. Gerado o id: {leitura_atuacao.id_leitura_atuacao}")

        return leitura_atuacao.id_leitura_atuacao  # Return the generated ID if needed

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Erro ocorreu ao processar o ack do acionamento do atuador: {str(e)}")
    finally:
        session.close()