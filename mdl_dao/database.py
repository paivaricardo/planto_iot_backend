from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


def create_session():
    # Carregar as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Recuperar as variáveis de ambiente e salvá-las em variáveis, para acesso ao banco de dados
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

