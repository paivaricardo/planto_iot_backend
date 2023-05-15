from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Perfil(Base):
    __tablename__ = 'tb_perfil'
    id_perfil = Column(Integer, primary_key=True)
    nome_perfil = Column(String(50), nullable=False)
