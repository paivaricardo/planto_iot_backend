import logging

from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError
from mdl_dao import database
from model.cultura_model import Cultura
from model.pydantic_rest_models.cultura_pydantic_model import CulturaPydanticModel
from model.sensor_atuador_model import SensorAtuador


def obter_todas_culturas(retrieve_status: bool = False):
    session = database.create_session()

    try:
        culturas = None

        if not retrieve_status:
            culturas = session.query(Cultura).all()
            return culturas
        else:
            culturas = session.query(Cultura,
                                     exists().where(SensorAtuador.id_cultura == Cultura.id_cultura).label('used')).all()

            for cultura, used in culturas:
                cultura.deletable = not used
                cultura.updatable = not used

            cultura_dicts = [
                {
                    'id_cultura': cultura.id_cultura,
                    'nome_cultura': cultura.nome_cultura,
                    'updatable': not used,
                    'deletable': not used,
                }
                for cultura, used in culturas
            ]

            return cultura_dicts

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao obter todas as culturas: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao obter todas as culturas: {str(e)}")

    finally:
        session.close()


def deletar_cultura(id_cultura: int):
    session = database.create_session()

    try:
        area = session.query(Cultura).filter(Cultura.id_cultura == id_cultura).first()

        if area is None:
            raise Exception(f"[DAO - ERRO] Cultura não encontrada com o id {id_cultura}")

        session.delete(area)
        session.commit()

        return True
    except SQLAlchemyError as e:
        session.rollback()

        logging.error(f"[DAO - ERRO] Erro ao tentar deletar a cultura na base de dados: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao tentar deletar a cultura na base de dados: {str(e)}")

    finally:
        session.close()


def criar_cultura(cultura: CulturaPydanticModel):
    session = database.create_session()

    try:
        cultura = Cultura(nome_cultura=cultura.nome_cultura)

        session.add(cultura)
        session.commit()

        return cultura
    except SQLAlchemyError as e:
        session.rollback()

        logging.error(f"[DAO - ERRO] Erro ao tentar criar a área na base de dados: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao tentar criar a área na base de dados: {str(e)}")

    finally:
        session.close()


def atualizar_cultura(id_cultura: int, cultura: CulturaPydanticModel):
    session = database.create_session()

    try:
        cultura_db = session.query(Cultura).filter(Cultura.id_cultura == id_cultura).first()

        if cultura_db is None:
            raise Exception(f"[DAO - ERRO] Cultura não encontrada com o id {id_cultura}")

        cultura_db.nome_cultura = cultura.nome_cultura

        session.commit()

        return cultura_db
    except SQLAlchemyError as e:
        session.rollback()

        logging.error(f"[DAO - ERRO] Erro ao tentar atualizar a cultura na base de dados: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao tentar atualizar a cultura na base de dados: {str(e)}")

    finally:
        session.close()


def obter_cultura_por_id_bd(id_cultura):
    session = database.create_session()

    try:
        area = session.query(Cultura).filter(Cultura.id_cultura == id_cultura).first()

        if area is None:
            raise Exception(f"[DAO - ERRO] Cultura não encontrada com o id {id_cultura}")

        return area

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao obter a cultura com o id {id_cultura}: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao obter a cultura com o id {id_cultura}: {str(e)}")

    finally:
        session.close()
