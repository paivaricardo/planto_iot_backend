from mdl_dao import dao_cultura


def obter_culturas_servico():
    return dao_cultura.obter_todas_culturas()