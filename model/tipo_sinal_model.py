from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TipoSinal(Base):
    __tablename__ = 'tb_tipo_sinal'

    id_tipo_sinal = Column(Integer, primary_key=True, autoincrement=True)
    nome_tipo_sinal = Column(String(50), nullable=False)
