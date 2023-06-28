from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from model.log_event_type_model import LogEventType
from model.usuario_model import Usuario

Base = declarative_base()


class Log(Base):
    __tablename__ = 'tb_log'

    id_log = Column(Integer, primary_key=True)
    data_hora_log = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    json_log = Column(Text)
    id_usuario = Column(Integer, ForeignKey(Usuario.id_usuario))
    id_log_event_type = Column(Integer, ForeignKey(LogEventType.id_log_event_type))

    usuario = relationship(Usuario)
    log_event_type = relationship(LogEventType)
