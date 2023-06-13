from sqlalchemy import Column, Integer, String, Float, Date, UniqueConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, column_property

from model.area_model import Area
from model.cultura_model import Cultura
from model.tipo_sensor_model import TipoSensor
from model.usuario_model import Usuario

Base = declarative_base()


class SensorAtuadorQueryModel(Base):
    __tablename__ = 'tb_sensor_atuador'

    id_sensor_atuador = Column(Integer, primary_key=True)
    uuid_sensor_atuador = Column(String(255), nullable=False)
    nome_sensor = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    data_cadastro_sensor = Column(Date)
    data_precadastro_sensor = Column(Date, nullable=False, server_default='CURRENT_DATE')

    # Chaves estrangeiras
    id_usuario_cadastrante = Column(Integer, ForeignKey(Usuario.id_usuario))
    id_area = Column(Integer, ForeignKey(Area.id_area))
    id_cultura = Column(Integer, ForeignKey(Cultura.id_cultura))
    id_tipo_sensor = Column(Integer, ForeignKey(TipoSensor.id_tipo_sensor))

    # Relacionamentos
    usuario_cadastrante = relationship(Usuario, lazy="joined")
    area = relationship(Area, lazy="joined")
    cultura = relationship(Cultura, lazy="joined")
    tipo_sensor = relationship(TipoSensor, lazy="joined")

    __table_args__ = (
        UniqueConstraint('uuid_sensor_atuador', name='idx_uuid_sensor'),
    )
