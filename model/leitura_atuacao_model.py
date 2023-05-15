from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from model.sensor_atuador_model import SensorAtuador
from model.tipo_sinal_model import TipoSinal

Base = declarative_base()


class LeituraAtuacao(Base):
    __tablename__ = 'tb_leitura_atuacao'
    id_leitura_atuacao = Column(Integer, primary_key=True)
    data_hora_leitura = Column(DateTime(timezone=True), nullable=False)
    json_leitura = Column(Text)
    id_sensor_atuador = Column(Integer, ForeignKey(SensorAtuador.id_sensor_atuador), nullable=False)
    id_tipo_sinal = Column(Integer, ForeignKey(TipoSinal.id_tipo_sinal), nullable=False)
