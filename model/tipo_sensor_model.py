from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TipoSensor(Base):
    __tablename__ = 'tb_tipo_sensor'

    id_tipo_sensor = Column(Integer, primary_key=True, autoincrement=True)
    nome_tipo_sensor = Column(String(255), nullable=False)
