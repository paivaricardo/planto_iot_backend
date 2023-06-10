from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from model.perfil_autorizacao_model import PerfilAutorizacao
from model.sensor_atuador_model import SensorAtuador
from model.usuario_model import Usuario

Base = declarative_base()


class AutorizacaoSensor(Base):
    __tablename__ = 'tb_autorizacao_sensor'
    id_autorizacao_sensor = Column(Integer, primary_key=True)
    id_sensor_atuador = Column(Integer, ForeignKey(SensorAtuador.id_sensor_atuador), nullable=False)
    id_usuario = Column(Integer, ForeignKey(Usuario.id_usuario), nullable=False)
    id_perfil_autorizacao = Column(Integer, ForeignKey(PerfilAutorizacao.id_perfil_autorizacao), nullable=False)
    visualizacao_ativa = Column(Boolean, nullable=False, default=False)
