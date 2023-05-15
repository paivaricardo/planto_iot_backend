from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Cultura(Base):
    __tablename__ = 'tb_cultura'
    id_cultura = Column(Integer, primary_key=True)
    nome_cultura = Column(String(255), nullable=False)
