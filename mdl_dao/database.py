from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session():
    connection_string = "postgresql://planto_iot_user:planto-iot-mariath@18.214.223.254:5432/db_planto_iot_sensores"
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
