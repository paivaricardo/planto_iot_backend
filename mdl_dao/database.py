from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


def create_session():
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    dbname = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')

    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

