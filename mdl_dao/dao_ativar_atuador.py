import json
import logging
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.leitura_atuacao_model import LeituraAtuacao
from model.sensor_atuador_model import SensorAtuador


def verificar_existencia_atuador_base_dados(uuid_informado: str):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Buscar se há uma correspondência do UUID informado para um atuador na base de dados
        atuador = session.query(SensorAtuador).filter(SensorAtuador.uuid_sensor_atuador == uuid_informado).first()

        if not atuador:
            logging.info(f"[DAO - INFO] Atuador com o UUID {uuid_informado} não encontrado no banco de dados.")
            return False
        else:
            logging.info(f"[DAO - INFO] Atuador com o UUID {uuid_informado} foi encontrado no banco de dados.")
            return True

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao verificar se o atuador existe na base de dados: {str(e)}")
        raise Exception("Erro ao verificar se o atuador existe na base de dados", str(e))
    finally:
        session.close()


def registrar_ativacao_atuador_base_dados(uuid_atuador: str, quantidade_atuacao: int):
    # Criar uma sessão para acesso ao banco de dados
    session = database.create_session()

    try:

        # Buscar se há uma correspondência do UUID informado para um atuador na base de dados
        atuador = session.query(SensorAtuador).filter(SensorAtuador.uuid_sensor_atuador == uuid_atuador).first()

        if not atuador:
            logging.error(f"[DAO - ERRO] Atuador com o UUID {uuid_atuador} não encontrado no banco de dados.")
            raise Exception(f"[DAO - ERRO] Atuador com o UUID {uuid_atuador} não encontrado no banco de dados.")

        leitura_atuacao = LeituraAtuacao(
            data_hora_leitura=datetime.now(),
            json_leitura=json.dumps({"quantidadeAtuacao": quantidade_atuacao}),
            id_sensor_atuador=atuador.id_sensor_atuador,
            id_tipo_sinal=50000,
        )

        session.add(leitura_atuacao)
        session.commit()

        logging.info(
            f"[DAO - INFO] Sinal de acionamento do atuador registrado com sucesso na base de dados. Gerado o id: {leitura_atuacao.id_leitura_atuacao}")

        return leitura_atuacao

    except SQLAlchemyError as e:
        session.rollback()

        logging.error(f"[DAO - ERRO] Erro ao tentar persistir a ativação da atuação na base de dados: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao tentar persistir a ativação da atuação na base de dados: {str(e)}")
    finally:
        session.close()
