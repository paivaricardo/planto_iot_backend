import logging

from mdl_dao import dao_autorizacao
from mdl_servicos import buscar_id_usuario_com_email_servico


def deletar_autorizacao_servico(id_autorizacao: int):
    autorizacao_deleted = dao_autorizacao.deletar_autorizacao_bd(id_autorizacao)
    return autorizacao_deleted


def criar_autorizacao_servico(id_sensor_atuador: int, id_usuario: int, id_perfil_autorizacao: int, conectar: bool):
    try:
        # Criar a autorização, chamando o DAO
        autorizacao_criada = dao_autorizacao.criar_autorizacao_bd(id_sensor_atuador, id_usuario, id_perfil_autorizacao,
                                                                  conectar)

        return autorizacao_criada
    except Exception as e:
        logging.error(f"[SERV - ERROR] Erro ao criar autorização: {str(e)}")
        raise e
