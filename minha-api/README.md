# ToDoList API

API REST para gerenciamento de tarefas, desenvolvida com **Python** e **FastAPI**.

## 🚀 Tecnologias utilizadas

- Python
- FastAPI
- Pydantic
- Uvicorn
- UV

## 📋 Funcionalidades

A API permite:

- Criar tarefas.
- Listar todas as tarefas.
- Consultar uma tarefa por ID.
- Atualizar tarefas.
- Excluir tarefas.
- Filtrar tarefas por status de conclusão.
- Filtrar tarefas por tag.
- Buscar tarefas pelo título.
- Ordenar tarefas.
- Utilizar paginação.
- Consultar tarefas por período de criação.

## 📦 Estrutura da tarefa

```json
{
  "id": 1,
  "titulo": "Estudar FastAPI",
  "descricao": "Aprender a criar APIs REST",
  "concluida": false,
  "tags": ["Python", "FastAPI"],
  "data_criacao": "2026-09-17T10:00:00",
  "data_atualizacao": "2026-09-17T10:00:00"
}
```

## ⚙️ Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/geovanysilvaa/TodoList-Api.git
```

### 2. Acessar a pasta do projeto

```bash
cd TodoList-Api/minha-api
```

### 3. Instalar as dependências

```bash
uv sync
```

### 4. Executar a API

```bash
uv run uvicorn main:app --reload
```

A API estará disponível em:

http://127.0.0.1:8000

## 📚 Documentação

A documentação interativa pode ser acessada pelo Swagger:

http://127.0.0.1:8000/docs

Também é possível acessar a documentação alternativa:

http://127.0.0.1:8000/redoc

## 🔗 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/tarefas` | Criar uma tarefa |
| GET | `/tarefas` | Listar tarefas |
| GET | `/tarefas/{id}` | Consultar tarefa por ID |
| PUT | `/tarefas/{id}` | Atualizar tarefa |
| DELETE | `/tarefas/{id}` | Excluir tarefa |

## 📝 Exemplo de criação de tarefa

**POST `/tarefas`**

```json
{
  "titulo": "Estudar Python",
  "descricao": "Revisar os conceitos de FastAPI",
  "tags": ["Python", "Estudos"]
}
```

## 🔍 Exemplos de filtros

Listar apenas tarefas concluídas:

```text
GET /tarefas?concluida=true
```

Filtrar por tag:

```text
GET /tarefas?tag=Python
```

Buscar pelo título:

```text
GET /tarefas?titulo=estudar
```

Ordenar por título em ordem decrescente:

```text
GET /tarefas?ordenar_por=titulo&ordem=desc
```

Utilizar paginação:

```text
GET /tarefas?pagina=1&limite=5
```

Combinar filtros:

```text
GET /tarefas?concluida=false&tag=Python&pagina=1&limite=10
```

## ⚠️ Observação

Atualmente, os dados são armazenados **em memória**. Portanto, as tarefas serão perdidas quando a aplicação for encerrada ou reiniciada.

## 👨‍💻 Autor

**Geovany de Oliveira Silva Batista**
**Jose Gabriel**
**Afonso Vanderlei**

Desenvolvido como atividade acadêmica do curso de **Análise e Desenvolvimento de Sistemas (ADS) — IFPI**.