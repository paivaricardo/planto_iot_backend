from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LogEventType(Base):
    __tablename__ = 'tb_log_event_type'

    id_log_event_type = Column(Integer, primary_key=True)
    nome_log_event_type = Column(String(255), nullable=False)
