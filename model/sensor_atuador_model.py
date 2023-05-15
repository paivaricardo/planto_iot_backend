from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SensorAtuador(Base):
    __tablename__ = 'tb_sensor_atuador'

    id_sensor_atuador = Column(Integer, primary_key=True)
    uuid_sensor_atuador = Column(String(255), nullable=False)
    nome_sensor = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    data_cadastro_sensor = Column(Date)
    data_precadastro_sensor = Column(Date, nullable=False, server_default='CURRENT_DATE')
    id_usuario_cadastrante = Column(Integer, ForeignKey('tb_usuario.id_usuario'))
    id_area = Column(Integer, ForeignKey('tb_area.id_area'))
    id_cultura = Column(Integer, ForeignKey('tb_cultura.id_cultura'))
    id_tipo_sensor = Column(Integer, ForeignKey('tb_tipo_sensor.id_tipo_sensor'))

    __table_args__ = (
        UniqueConstraint('uuid_sensor_atuador', name='idx_uuid_sensor'),
    )