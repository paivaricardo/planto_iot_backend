from mdl_dao import dao_area
from model.pydantic_rest_models.area_pydantic_model import AreaPydanticModel


def obter_areas_servico(retrieve_status: bool = False):
    return dao_area.obter_todas_areas(retrieve_status)


def deletar_area_servico(id_area: int):
    return dao_area.deletar_area(id_area)


def criar_area_servico(area: AreaPydanticModel):
    return dao_area.criar_area(area)


def atualizar_area_servico(id_area: int, area: AreaPydanticModel):
    return dao_area.atualizar_area(id_area, area)


def obter_area_por_id_servico(id_area: int):
    return dao_area.obter_area_por_id_bd(id_area)