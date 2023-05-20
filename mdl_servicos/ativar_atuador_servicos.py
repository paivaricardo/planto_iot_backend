from mdl_dao import dao_ativar_atuador
from mdl_interacao_sensores_atuadores import interacao_com_atuadores

def verificar_existencia_atuador_servico(uuid: str):
    """
    Verifica se um atuador existe na base de dados.

    Retorna True se o atuador existe e False se não existe.
    """
    try:
        # Chamar o DAO para verificar se o atuador existe na base de dados
        atuador_existe = dao_ativar_atuador.verificar_existencia_atuador_base_dados(uuid)

        return atuador_existe
    except Exception as e:
        raise Exception("Erro ao verificar se o atuador existe na base de dados", str(e))


def ativar_atuador_servico(uuid_atuador: str, quantidade_atuacao: int):
    """
    Ativa o módulo para interação com o atuador, para ativação de um atuador específico no Planto IoT.
    """
    try:
        # Chamar o DAO para ativar o atuador
        interacao_atuador_bem_sucedida = interacao_com_atuadores.enviar_sinal_atuador(uuid_atuador, quantidade_atuacao)

        return interacao_atuador_bem_sucedida
    except Exception as e:
        raise Exception("Erro ao ativar o atuador", str(e))