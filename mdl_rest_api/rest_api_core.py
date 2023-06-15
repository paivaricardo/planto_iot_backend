import logging
from uuid import UUID

from fastapi import FastAPI, HTTPException, Response

from mdl_servicos import precadastrar_sensor_atuador_servicos, verificar_sensor_atuador_servicos, \
    ativar_atuador_servicos, cadastrar_sensor_atuador_servicos, conectar_usuario_sensor_servicos, \
    verificar_cadastrar_usuario_servicos, listar_sensores_atuadores_conectados_servicos
from model.pydantic_rest_models.sensor_atuador_cadastro_completo_rest_model import SensorAtuadorCadastroCompleto
from model.pydantic_rest_models.usuario_rest_model import UsuarioRestModel

app = FastAPI()


@app.get("/health-check")
def health_check():
    """
    Realiza um health check da aplicação, indicando se está online ou não.
    """
    return {"status": "ok"}


@app.get("/pre-cadastrar-sensor-atuador")
def precadastrar_sensor_ou_atuador(id_tipo_sensor: int):
    """
    Precadastra um sensor ou um atuador na base de dados.

    Requer, para o precadastro, um id tipo de sensor ou atuador
    """
    try:

        # Chamar a chamada de serviços para precadastrar um sensor ou um atuador
        uuid_gerado = precadastrar_sensor_atuador_servicos.precadastrar_sensor_atuador_servico(id_tipo_sensor)

        return Response(content={"status": "pre-cadastrado", "uuid": uuid_gerado}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail={"message": "Erro ao precadastrar o sensor ou atuador", "error": str(e)})


@app.get("/ativar-atuador/{uuid}")
def ativar_atuador(uuid: UUID, quantidade_atuacao: int):
    """
    Envia sinal para ativação de um atuador específico no Planto IoT. O sinal é direcionado ao atuador com o uuid informado. A intensidade de ativação de um atuador é definida por meio de um queryParam de quantidade_atuacao.
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

        return {"message": "Sinal para ativação da atuação completado com sucesso", "uuid": uuid,
                "quantidade_atuacao": quantidade_atuacao}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail={"message": "Erro ao enviar sinal para ativação da autação", "error": str(e)})


@app.get("/verificar-sensor-atuador/{uuid}")
def verificar_sensor_atuador(uuid: UUID):
    """
    Verifica se um sensor ou um atuador existe na base de dados e se já foi cadastrado no Planto IoT. Útil no processo de realizar uma conexão ao sensor ou para redirecionar a uma tela de cadastro.

    Existem 3 hipóteses:
    1. O sensor ou atuador existe na base de dados (pré-cadastro) e já foi cadastrado no Planto IoT
    Nesse caso, caso a pessoa possua permissão de acesso ao sensor, ela será conectada imediatamente ao sensor ou ao atuador.

    2. O sensor ou atuador existe na base de dados (pré-cadastro), mas ainda não foi cadastrado no Planto IoT
    Nesse caso, a pessoa será redirecionada a uma tela de cadastro, para completar o cadastro do sensor ou atuador no Planto IoT, contanto que ela possua permissão de acesso ao sensor.

    3. O sensor ou atuador não existe na base de dados (pré-cadastro)
    Nesse caso, será mostrada uma informação de que o sensor ou atuador não foi precadastrado e não consta na base de dados. Será orientada a procurar por um representante da empresa (para que a empresa realize o pré-cadastro).

    """
    try:
        if not uuid:
            raise Exception("UUID não informado")

        # Chamar camada de serviços para verificar se o sensor ou atuador realmente existe na base de dados
        sensor_atuador_status = verificar_sensor_atuador_servicos.verificar_existencia_sensor_atuador_servico(str(uuid))

        if not sensor_atuador_status or not sensor_atuador_status["sensor_atuador_existe_bd"]:
            raise Exception("O sensor ou atuador informado não existe na base de dados")

        return sensor_atuador_status
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail={"message": "Erro ao verificar se o sensor ou atuador existe na base de dados",
                                    "error": str(e)})


@app.post("/cadastrar-sensor-atuador")
def cadastrar_sensor_atuador(sensor_atuador_cadastro_completo: SensorAtuadorCadastroCompleto):
    """
    Cadastra um sensor ou um atuador na base de dados do Planto IoT, completando os dados da tabela de sensores ou atuadores (tb_sensor_atuador).

    """

    try:
        if not sensor_atuador_cadastro_completo.uuid_sensor_atuador:
            raise Exception("UUID não informado")

        # Chamar camada de serviços para verificar se o sensor ou atuador realmente existe na base de dados
        sensor_atuador_status = verificar_sensor_atuador_servicos.verificar_existencia_sensor_atuador_servico(
            sensor_atuador_cadastro_completo.uuid_sensor_atuador)

        if not sensor_atuador_status or not sensor_atuador_status["sensor_atuador_existe_bd"]:
            raise Exception("O sensor ou atuador informado não existe na base de dados (não foi precadastrado")

        # Chamar camada de serviços para cadastrar o sensor ou atuador na base de dados
        sensor_atuador_cadastrado = cadastrar_sensor_atuador_servicos.cadastrar_sensor_atuador_sevico(
            sensor_atuador_cadastro_completo)

        if sensor_atuador_cadastrado:
            # Chamar a camada de serviços para conectar o usuário ao sensor (tabela tb_autorizacao_sensor)
            sensor_atuador_conectado = conectar_usuario_sensor_servicos.conectar_usuario_sensor_servico(
                sensor_atuador_cadastro_completo.uuid_sensor_atuador,
                sensor_atuador_cadastro_completo.id_usuario_cadastrante)

            return {
                "message": f"Sensor ou atuador de UUID {sensor_atuador_cadastro_completo.uuid_sensor_atuador} cadastrado com sucesso",
                "conexao_usuario_sensor": sensor_atuador_conectado}
        else:
            return {
                "message": f"Erro ao cadastrar o sensor ou atuador de UUID {sensor_atuador_cadastro_completo.uuid_sensor_atuador}"}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail={"message": "Erro ao tentar cadastrar o sensor ou atuador na base de dados",
                                    "error": str(e)})


@app.post("/verificar-cadastrar-usuario")
def verificar_cadastrar_usuario(usuario_rest_model: UsuarioRestModel):
    """
    Verifica se um usuário existe na base de dados do Planto Iot, com base no e-mail fornecido. Se ele não existir, um novo cadastro é realizado para esse usuário. É devolvido um id de usuário (verificado ou cadastrado), para utilização na aplicação.
    """

    logging.info(f"[REST - INFO] Iniciando a verificação de cadastro do usuário {usuario_rest_model.nome_usuario} (email {usuario_rest_model.email_usuario})")

    try:
        if not usuario_rest_model.email_usuario:
            raise Exception("E-mail não informado")

        if not usuario_rest_model.nome_usuario:
            raise Exception("Nome do usuário não informado")

        if not usuario_rest_model.id_perfil:
            raise Exception("Perfil do usuário não informado")

        # Chamar camada de serviços para verificar se o sensor ou atuador realmente existe na base de dados
        usuario_status = verificar_cadastrar_usuario_servicos.verificar_cadastrar_usuario_servico(usuario_rest_model)

        if usuario_status["usuario_ja_existe_bd"]:
            return {
                "message": f"Usuário com o e-mail: {usuario_rest_model.email_usuario} já existe na base de dados.",
                "usuario": usuario_status["usuario_cadastrado"]}
        else:
            message_string = f"Usuário com o e-mail: {usuario_rest_model.email_usuario} não existia na base de dados. Usuário cadastrado com sucesso."
            usuario_status = usuario_status["usuario_cadastrado"]

            return {
                "message": message_string,
                "usuario": usuario_status}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail={"message": "Erro ao tentar verificar ou cadastrar o usuário na base de dados",
                                    "error": str(e)})


@app.get("/listar-sensores-atuadores-conectados")
def listar_sensores_atuadores_conectados(email_usuario: str):
    """
    Retorna uma lista de todos os sensores e atuadores que estão conectados a determinado usuário (atributo visualizacao_ativa da tb_autorizacao_sensor setado como True).
    """

    try:
        if not email_usuario:
            raise Exception("Email do usuário não informado")

        # Chamar camada de serviços para obter uma lista de todos os sensores e atuadores conectados a um determinado usuário
        listar_sensores_atuadores_conectados = listar_sensores_atuadores_conectados_servicos.listar_sensores_atuadores_conectados_servico(email_usuario)

        return listar_sensores_atuadores_conectados
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail={"message": "Erro ao tentar listar os sensores e atuadores conectados ao usuário na base de dados",
                                    "error": str(e)})
