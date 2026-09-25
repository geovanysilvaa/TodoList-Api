import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app, tarefas_db

@pytest.fixture
def client():
    tarefas_db.clear()

    with TestClient(app) as client:
        yield client

    tarefas_db.clear()


@pytest.fixture
def tarefas_iniciais(client):
    tarefas = [
        {
            "titulo": "Estudar Python",
            "descricao": "Aprender Python",
            "tags": ["python", "estudos"],
        },
        {
            "titulo": "Fazer exercícios",
            "descricao": "Resolver exercícios",
            "tags": ["python"],
        },
        {
            "titulo": "Estudar FastAPI",
            "descricao": "Criar API",
            "tags": ["fastapi"],
        },
    ]

    respostas = []

    for tarefa in tarefas:
        resposta = client.post("/tarefas", json=tarefa)
        respostas.append(resposta.json())

    # Concluir a segunda tarefa
    client.put(
        f"/tarefas/{respostas[1]['id']}",
        json={
            "titulo": respostas[1]["titulo"],
            "descricao": respostas[1]["descricao"],
            "concluida": True,
            "tags": respostas[1]["tags"],
        },
    )

    return respostas
