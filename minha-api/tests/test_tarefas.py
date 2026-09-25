import pytest


CAMPOS = {
    "id",
    "titulo",
    "descricao",
    "concluida",
    "tags",
    "data_criacao",
    "data_atualizacao",
}


# ==================== CRIAÇÃO ====================

def test_criar_tarefa(client):
    response = client.post(
        "/tarefas",
        json={
            "titulo": "Estudar Python",
            "descricao": "Estudar testes",
            "tags": ["python", "pytest"],
        },
    )

    assert response.status_code == 200

    tarefa = response.json()

    assert CAMPOS <= tarefa.keys()
    assert tarefa["id"] is not None
    assert tarefa["concluida"] is False
    assert tarefa["tags"] == ["python", "pytest"]
    assert tarefa["data_criacao"] is not None
    assert tarefa["data_atualizacao"] is not None


def test_criar_sem_titulo(client):
    response = client.post(
        "/tarefas",
        json={
            "descricao": "Sem título",
            "tags": [],
        },
    )

    assert response.status_code == 422


# ==================== CONSULTA ====================

def test_listar_tarefas_vazio(client):
    response = client.get("/tarefas")

    assert response.status_code == 200
    assert response.json()["tarefas"] == []
    assert response.json()["total"] == 0


def test_listar_tarefas(client, tarefas_iniciais):
    response = client.get("/tarefas")

    assert response.status_code == 200

    dados = response.json()

    assert dados["total"] == 3
    assert len(dados["tarefas"]) == 3

    for tarefa in dados["tarefas"]:
        assert CAMPOS <= tarefa.keys()


def test_consultar_tarefa(client):
    criar = client.post(
        "/tarefas",
        json={"titulo": "Teste", "descricao": "Descrição"},
    )

    tarefa_id = criar.json()["id"]

    response = client.get(f"/tarefas/{tarefa_id}")

    assert response.status_code == 200
    assert response.json()["id"] == tarefa_id
    assert response.json()["titulo"] == "Teste"


def test_consultar_tarefa_inexistente(client):
    response = client.get("/tarefas/9999")

    assert response.status_code == 404


# ==================== ATUALIZAÇÃO ====================

def test_atualizar_tarefa(client):
    criar = client.post(
        "/tarefas",
        json={
            "titulo": "Título antigo",
            "descricao": "Descrição antiga",
            "tags": ["python"],
        },
    )

    tarefa = criar.json()
    tarefa_id = tarefa["id"]
    data_criacao = tarefa["data_criacao"]

    response = client.put(
        f"/tarefas/{tarefa_id}",
        json={
            "titulo": "Título novo",
            "descricao": "Descrição nova",
            "concluida": True,
            "tags": ["python", "fastapi"],
        },
    )

    assert response.status_code == 200

    atualizada = response.json()

    assert atualizada["titulo"] == "Título novo"
    assert atualizada["descricao"] == "Descrição nova"
    assert atualizada["concluida"] is True
    assert atualizada["tags"] == ["python", "fastapi"]
    assert atualizada["data_criacao"] == data_criacao
    assert atualizada["data_atualizacao"] != data_criacao


def test_atualizar_tarefa_inexistente(client):
    response = client.put(
        "/tarefas/9999",
        json={
            "titulo": "Teste",
            "descricao": "",
            "concluida": False,
            "tags": [],
        },
    )

    assert response.status_code == 404


# ==================== EXCLUSÃO ====================

def test_excluir_tarefa(client):
    criar = client.post(
        "/tarefas",
        json={"titulo": "Excluir"},
    )

    tarefa_id = criar.json()["id"]

    response = client.delete(f"/tarefas/{tarefa_id}")

    assert response.status_code == 204

    assert client.get(f"/tarefas/{tarefa_id}").status_code == 404


def test_excluir_tarefa_inexistente(client):
    response = client.delete("/tarefas/9999")

    assert response.status_code == 404


# ==================== FILTROS ====================

@pytest.mark.parametrize(
    "filtro,valor,esperado",
    [
        ("concluida", "true", True),
        ("concluida", "false", False),
    ],
)
def test_filtro_concluida(
    client, tarefas_iniciais, filtro, valor, esperado
):
    response = client.get(f"/tarefas?{filtro}={valor}")

    assert response.status_code == 200

    for tarefa in response.json()["tarefas"]:
        assert tarefa["concluida"] is esperado


def test_filtro_tag(client, tarefas_iniciais):
    response = client.get("/tarefas?tag=python")

    assert response.status_code == 200

    tarefas = response.json()["tarefas"]

    assert len(tarefas) > 0

    for tarefa in tarefas:
        assert "python" in tarefa["tags"]


def test_filtro_tag_sem_resultado(client, tarefas_iniciais):
    response = client.get("/tarefas?tag=java")

    assert response.status_code == 200
    assert response.json()["tarefas"] == []


def test_filtro_titulo(client, tarefas_iniciais):
    response = client.get("/tarefas?titulo=python")

    assert response.status_code == 200

    tarefas = response.json()["tarefas"]

    for tarefa in tarefas:
        assert "python" in tarefa["titulo"].lower()


def test_filtro_titulo_sem_resultado(client, tarefas_iniciais):
    response = client.get("/tarefas?titulo=xyz")

    assert response.status_code == 200
    assert response.json()["tarefas"] == []


# ==================== COMBINAÇÃO ====================

def test_combinar_filtros(client, tarefas_iniciais):
    response = client.get(
        "/tarefas?concluida=false&tag=python"
    )

    assert response.status_code == 200

    for tarefa in response.json()["tarefas"]:
        assert tarefa["concluida"] is False
        assert "python" in tarefa["tags"]


# ==================== ORDENAÇÃO ====================

@pytest.mark.parametrize(
    "campo,ordem",
    [
        ("id", "asc"),
        ("id", "desc"),
        ("titulo", "asc"),
        ("titulo", "desc"),
        ("data_criacao", "asc"),
        ("data_criacao", "desc"),
        ("data_atualizacao", "asc"),
        ("data_atualizacao", "desc"),
    ],
)
def test_ordenacao(client, tarefas_iniciais, campo, ordem):
    response = client.get(
        f"/tarefas?ordenar_por={campo}&ordem={ordem}"
    )

    assert response.status_code == 200

    tarefas = response.json()["tarefas"]
    valores = [tarefa[campo] for tarefa in tarefas]

    assert valores == sorted(
        valores,
        reverse=(ordem == "desc"),
    )


# ==================== VALIDAÇÃO ====================

def test_concluida_invalida(client):
    response = client.get("/tarefas?concluida=abc")

    assert response.status_code == 422


def test_ordenacao_invalida(client):
    response = client.get(
        "/tarefas?ordenar_por=invalido"
    )

    assert response.status_code == 422


def test_ordem_invalida(client):
    response = client.get(
        "/tarefas?ordem=invalida"
    )

    assert response.status_code == 422
