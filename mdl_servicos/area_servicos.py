from mdl_dao import dao_area


def obter_areas_servico(retrieve_status: bool = False):
    return dao_area.obter_todas_areas(retrieve_status)


def deletar_area_servico(id_area):
    return dao_area.deletar_area(id_area)