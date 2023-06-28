import logging

from mdl_dao import dao_log
from mdl_servicos import buscar_id_usuario_com_email_servicos


def registrar_login_usuario_log_servico(email_usuario: str):
    try:
        id_usuario = buscar_id_usuario_com_email_servicos.buscar_id_usuario_com_email_servico(email_usuario)

        dao_log.registrar_login_usuario_log_bd(id_usuario)

    except Exception as e:
        logging.error(f"[LOG - SERVICO - ERROR] Erro ao registrar login do usuário {email_usuario}: {e}")