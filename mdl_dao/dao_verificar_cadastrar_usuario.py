import logging

from sqlalchemy.exc import SQLAlchemyError

from mdl_dao import database
from model.pydantic_rest_models.usuario_rest_model import UsuarioRestModel
from model.usuario_model import Usuario


def cadastrar_usuario_base_dados(usuario_rest_model: UsuarioRestModel):
    try:
        # Criar uma sessão para acesso ao banco de dados
        session = database.create_session()

        # Instanciar um objeto de usuário segundo o model de usuário do SQLAlchemy (Usuario)
        usuario_cadastro = Usuario(
            email_usuario=usuario_rest_model.email_usuario,
            nome_usuario=usuario_rest_model.nome_usuario,
            id_perfil=usuario_rest_model.id_perfil,
        )

        # Fazer o update com base nas novas informações de cadastro fornecidas
        session.add(usuario_cadastro)

        # Fazer o commit das alterações no banco de dados
        session.commit()

        logging.info(
            f"[DAO - INFO] Usuário cadastrado com o id: {str(usuario_cadastro.id_usuario)}")

        return {"id_usuario": usuario_cadastro.id_usuario, "email_usuario": usuario_cadastro.email_usuario,
                "nome_usuario": usuario_cadastro.nome_usuario,
                "data_cadastro": usuario_cadastro.data_cadastro, "id_perfil": usuario_cadastro.id_perfil}

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao tentar cadastrar o usuário na base de dados: {str(e)}")
        raise Exception(f"Erro ao tentar cadastrar o usuário na base de dados: {str(e)}")


def verificar_usuario_base_dados(usuario_rest_model):
    try:
        # Criar uma sessão para acesso ao banco de dados
        session = database.create_session()

        # Consultar a base de dados, para ver se o usuário foi localizado. Se não for, o método first() retorna None
        usuario_busca = session.query(Usuario).filter(
            Usuario.email_usuario == usuario_rest_model.email_usuario).first()

        if usuario_busca is None:
            logging.info(
                f"[DAO - INFO] Usuário com o email {usuario_rest_model.email_usuario} não encontrado na base de dados.")
            return None
        else:
            logging.info(
                f"[DAO - INFO] Usuário com o e-mail {usuario_rest_model.email_usuario} foi encontrado na base de dados com o id: {str(usuario_busca.id_usuario)}")
            return {"id_usuario": usuario_busca.id_usuario, "email_usuario": usuario_busca.email_usuario,
                    "nome_usuario": usuario_busca.nome_usuario,
                    "data_cadastro": usuario_busca.data_cadastro, "id_perfil": usuario_busca.id_perfil}

    except SQLAlchemyError as e:
        logging.error(f"[DAO - ERRO] Erro ao tentar verificar se o usuário existe na base de dados: {str(e)}")
        raise Exception(f"Erro ao tentar verificar se o usuário existe na base de dados: {str(e)}")
