from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LeituraAtuacao(Base):
    __tablename__ = 'tb_leitura_atuacao'
    id_leitura_atuacao = Column(Integer, primary_key=True)
    data_hora_leitura = Column(DateTime(timezone=True), nullable=False)
    json_leitura = Column(Text)
    id_sensor_atuador = Column(Integer, ForeignKey('tb_sensor_atuador.id_sensor_atuador'), nullable=False)
    id_tipo_sinal = Column(Integer, ForeignKey('tb_tipo_sinal.id_tipo_sinal'), nullable=False)
