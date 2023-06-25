from mdl_dao import dao_buscar_id_usuario_com_email


def buscar_id_usuario_com_email(email_usuario: str):
    return dao_buscar_id_usuario_com_email.buscar_id_usuario_com_email(email_usuario)
