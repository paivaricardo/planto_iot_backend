from uuid import UUID

from fastapi import FastAPI, HTTPException

from mdl_servicos import precadastrar_sensor_atuador_servicos, ativar_atuador_servicos

app = FastAPI()


@app.get("/health-check")
def health_check():
    """
    Realiza um health check da aplicação, indicando se está online ou não.
    """
    return {"status": "ok"}

@app.get("/pre-cadastrar-sensor-atuador")
def cadastrar_sensor_ou_atuador(id_tipo_sensor: int):
    """
    Precadastra um sensor ou um atuador na base de dados.

    Requer, para o precadastro, um id tipo de sensor ou atuador
    """
    try:

        # Chamar a chamada de serviços para precadastrar um sensor ou um atuador
        uuid_gerado = precadastrar_sensor_atuador_servicos.precadastrar_sensor_atuador_servico(id_tipo_sensor)

        return {"status": "pre-cadastrado", "uuid": uuid_gerado}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail={"message": "Erro ao precadastrar o sensor ou atuador", "error": str(e)})
@app.get("/ativar-atuador/{uuid}")
def ativar_atuador(uuid: UUID, quantidade_atuacao: int):
    """
    Envia um sinal para acionamento de um atuador específico no Planto IoT.
    """
    try:
        if not uuid:
            raise Exception("UUID não informado")
        if not quantidade_atuacao:
            raise Exception("Quantidade de atuação não informada")

        # Chamar camada de serviços para verificar se o atuador realmente existe na base de dados
        atuador_existe = ativar_atuador_servicos.verificar_existencia_atuador_servico(str(uuid))

        if not atuador_existe:
            raise Exception("O atuador informado não existe na base de dados")

        # Chamar camada de serviços para iniciar o sinal para a atuação
        interacao_atuador_bem_sucedida = ativar_atuador_servicos.ativar_atuador_servico(str(uuid), quantidade_atuacao)

        if not interacao_atuador_bem_sucedida:
            raise Exception("Erro ao enviar sinal para ativação da atuação")

        return {"message": "Sinal para ativação da atuação completado com sucesso", "uuid": uuid, "quantidade_atuacao": quantidade_atuacao}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": "Erro ao enviar sinal para ativação da autação", "error": str(e)})