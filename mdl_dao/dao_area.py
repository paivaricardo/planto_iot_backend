import logging

from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.area_model import Area
from model.pydantic_rest_models.area_pydantic_model import AreaPydanticModel
from model.sensor_atuador_model import SensorAtuador


def obter_todas_areas(retrieve_status: bool = False):
    session = database.create_session()

    try:
        areas = None

        if not retrieve_status:
            areas = session.query(Area).all()
            return areas
        else:
            areas = session.query(Area, exists().where(SensorAtuador.id_area == Area.id_area).label('used')).all()

            for area, used in areas:
                area.deletable = not used
                area.updatable = not used

            area_dicts = [
                {
                    'id_area': area.id_area,
                    'nome_area': area.nome_area,
                    'updatable': not used,
                    'deletable': not used,
                }
                for area, used in areas
            ]

            return area_dicts

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao obter todas as áreas: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao obter todas as áreas: {str(e)}")

    finally:
        session.close()


def deletar_area(id_area):
    session = database.create_session()

    try:
        area = session.query(Area).filter(Area.id_area == id_area).first()

        if area is None:
            raise Exception(f"[DAO - ERRO] Área não encontrada com o id {id_area}")

        session.delete(area)
        session.commit()

        return True
    except SQLAlchemyError as e:
        session.rollback()

        logging.error(f"[DAO - ERRO] Erro ao tentar deletar a área na base de dados: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao tentar deletar a área na base de dados: {str(e)}")

    finally:
        session.close()


def criar_area(area: AreaPydanticModel):
    session = database.create_session()

    try:
        area = Area(nome_area=area.nome_area)

        session.add(area)
        session.commit()

        return area
    except SQLAlchemyError as e:
        session.rollback()

        logging.error(f"[DAO - ERRO] Erro ao tentar criar a área na base de dados: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao tentar criar a área na base de dados: {str(e)}")

    finally:
        session.close()


def atualizar_area(id_area: int, area: AreaPydanticModel):
    session = database.create_session()

    try:
        area_db = session.query(Area).filter(Area.id_area == id_area).first()

        if area_db is None:
            raise Exception(f"[DAO - ERRO] Área não encontrada com o id {id_area}")

        area_db.nome_area = area.nome_area

        session.commit()

        return area_db
    except SQLAlchemyError as e:
        session.rollback()

        logging.error(f"[DAO - ERRO] Erro ao tentar atualizar a área na base de dados: {str(e)}")
        raise Exception(f"[DAO - ERRO] Erro ao tentar atualizar a área na base de dados: {str(e)}")

    finally:
        session.close()
