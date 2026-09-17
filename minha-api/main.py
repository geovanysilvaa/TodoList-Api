from datetime import datetime, date
from typing import List, Literal, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()


# ---------- Modelos ----------

class TarefaCriar(BaseModel):
    titulo: str
    descricao: str = ""
    tags: List[str] = []


class TarefaAtualizar(BaseModel):
    titulo: str
    descricao: str = ""
    concluida: bool = False
    tags: List[str] = []


# ---------- "Banco" em memória ----------

tarefas_db = []
proximo_id = 1


# ---------- Criar tarefa ----------

@app.get("/")
def inicio():
    return {
        "mensagem": "API To-Do funcionando!",
        "documentacao": "/docs"
    }

@app.post("/tarefas")
def criar_tarefa(tarefa: TarefaCriar):
    global proximo_id
    agora = datetime.now()

    nova_tarefa = {
        "id": proximo_id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "concluida": False,
        "tags": tarefa.tags,
        "data_criacao": agora,
        "data_atualizacao": agora,
    }

    tarefas_db.append(nova_tarefa)
    proximo_id += 1
    return nova_tarefa


# ---------- Listar tarefas (com filtros, ordenação e paginação) ----------

@app.get("/tarefas")
def listar_tarefas(
    concluida: Optional[bool] = None,
    tag: Optional[str] = None,
    titulo: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    ordenar_por: Literal["id", "titulo", "data_criacao", "data_atualizacao"] = "id",
    ordem: Literal["asc", "desc"] = "asc",
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
):
    resultado = tarefas_db

    if concluida is not None:
        resultado = [t for t in resultado if t["concluida"] == concluida]

    if tag is not None:
        resultado = [t for t in resultado if tag in t["tags"]]

    if titulo is not None:
        resultado = [t for t in resultado if titulo.lower() in t["titulo"].lower()]

    if data_inicio is not None:
        resultado = [t for t in resultado if t["data_criacao"].date() >= data_inicio]

    if data_fim is not None:
        resultado = [t for t in resultado if t["data_criacao"].date() <= data_fim]

    resultado = sorted(resultado, key=lambda t: t[ordenar_por], reverse=(ordem == "desc"))

    total = len(resultado)
    inicio = (pagina - 1) * limite
    fim = inicio + limite

    return {
        "pagina": pagina,
        "limite": limite,
        "total": total,
        "tarefas": resultado[inicio:fim],
    }


# ---------- Consultar uma tarefa ----------

@app.get("/tarefas/{id}")
def obter_tarefa(id: int):
    for tarefa in tarefas_db:
        if tarefa["id"] == id:
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


# ---------- Atualizar uma tarefa ----------

@app.put("/tarefas/{id}")
def atualizar_tarefa(id: int, dados: TarefaAtualizar):
    for tarefa in tarefas_db:
        if tarefa["id"] == id:
            tarefa["titulo"] = dados.titulo
            tarefa["descricao"] = dados.descricao
            tarefa["concluida"] = dados.concluida
            tarefa["tags"] = dados.tags
            tarefa["data_atualizacao"] = datetime.now()
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


# ---------- Excluir uma tarefa ----------

@app.delete("/tarefas/{id}", status_code=204)
def excluir_tarefa(id: int):
    for i, tarefa in enumerate(tarefas_db):
        if tarefa["id"] == id:
            tarefas_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")