from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AutorizacaoSensor(Base):
    __tablename__ = 'tb_autorizacao_sensor'
    id_autorizacao_sensor = Column(Integer, primary_key=True)
    id_sensor_atuador = Column(Integer, ForeignKey('tb_sensor_atuador.id_sensor_atuador'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('tb_usuario.id_usuario'), nullable=False)
    id_perfil_autorizacao = Column(Integer, ForeignKey('tb_perfil_autorizacao.id_perfil_autorizacao'), nullable=False)
    visualizacao_ativa = Column(Boolean, nullable=False, default=False)
