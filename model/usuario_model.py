from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'tb_usuario'
    id_usuario = Column(Integer, primary_key=True)
    email_usuario = Column(String(255), nullable=False)
    nome_usuario = Column(String(255), nullable=False)
    data_cadastro = Column(Date, nullable=False)
    id_perfil = Column(Integer, ForeignKey('tb_perfil.id_perfil'), nullable=False)