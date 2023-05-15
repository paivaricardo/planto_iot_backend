from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Area(Base):
    __tablename__ = 'tb_area'
    id_area = Column(Integer, primary_key=True)
    nome_area = Column(String(255), nullable=False)
