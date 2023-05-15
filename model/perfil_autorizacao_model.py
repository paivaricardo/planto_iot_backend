from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PerfilAutorizacao(Base):
    __tablename__ = 'tb_perfil_autorizacao'
    id_perfil_autorizacao = Column(Integer, primary_key=True)
    nme_perfil_autorizacao = Column(String(100), nullable=False)
