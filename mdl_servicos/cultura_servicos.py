from mdl_dao import dao_cultura
from model.pydantic_rest_models.cultura_pydantic_model import CulturaPydanticModel


def obter_culturas_servico(retrieve_status: bool = False):
    return dao_cultura.obter_todas_culturas(retrieve_status)


def deletar_cultura_servico(id_cultura: int):
    return dao_cultura.deletar_cultura(id_cultura)


def criar_cultura_servico(cultura: CulturaPydanticModel):
    return dao_cultura.criar_cultura(cultura)


def atualizar_cultura_servico(id_cultura, cultura):
    return dao_cultura.atualizar_cultura(id_cultura, cultura)