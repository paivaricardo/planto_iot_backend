import logging


def validar_uuid_sensor_atuador(mensagem_dict):
    # Validar se o uuid do sensor ou atuador é válido e está cadastrado no banco de dados
    # TODO: Implementar validação de uuid do sensor ou atuador
    if not mensagem_dict["uuidSensorAtuador"]:
        logging.error("[PROC MENSAGENS - ERRO] Uuid do sensor não informado na mensagem.")
        return False

    return True


def validar_consistencia_atributos_sensor(mensagem_dict):
    # Validar se os atributos do sensor são consistentes e correspondem ao que está cadastrado no banco de dados
    # TODO: Implementar validação da consistência de atributos do sensor
    return True


def validar_consistencia_dados_sensor(mensagem_dict):
    # Validar se os dados enviados pelo sensor estão consistentes e dentro dos limites razoáveis
    # TODO: Implementar validação da consistência de dados do sensor
    return True
