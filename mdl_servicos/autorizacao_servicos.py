import logging

from mdl_dao import dao_autorizacao
from mdl_servicos import buscar_id_usuario_com_email_servicos
from model.pydantic_rest_models.autorizacao_pydantic_model import AutorizacaoPydanticModel


def deletar_autorizacao_servico(id_autorizacao: int):
    autorizacao_deleted = dao_autorizacao.deletar_autorizacao_bd(id_autorizacao)
    return autorizacao_deleted


def criar_autorizacao_servico(autorizacao_pydantic_model: AutorizacaoPydanticModel):
    try:
        id_usuario = buscar_id_usuario_com_email_servicos.buscar_id_usuario_com_email_servico(autorizacao_pydantic_model.email_usuario)

        # Se o usuário não existir, retorna o status 1
        if id_usuario is None:
            return 1

        # Criar a autorização, chamando o DAO
        autorizacao_criada = dao_autorizacao.criar_autorizacao_bd(autorizacao_pydantic_model, id_usuario)

        return autorizacao_criada
    except Exception as e:
        logging.error(f"[SERV - ERROR] Erro ao criar autorização: {str(e)}")
        raise e
