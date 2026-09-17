Checklist de testes

# 1. Criar tarefas — POST /tarefas

 Criar com este JSON, deve dar 201:
``` json
{"titulo": "Estudar FastAPI", "descricao": "Revisar rotas", "tags": ["python", "fastapi"]}
 Criar mais 2 tarefas diferentes (mude título e tags), pra ter dados pra testar os filtros. Ex:

{"titulo": "Estudar Python", "descricao": "Funções e classes", "tags": ["python", "estudos"]}

{"titulo": "Exercícios de Python", "descricao": "Lista de exercícios", "tags": ["python", "exercicios"]}
```
2. Listar todas — GET /tarefas

 Execute sem preencher nada. Deve dar 200 e devolver as 3 tarefas dentro de "tarefas".

3. Consultar uma tarefa — GET /tarefas/{id}

 Coloque id = 1 → deve dar 200.
 Coloque id = 9999 (que não existe) → deve dar 404.

4. Atualizar — PUT /tarefas/{id}

 Em id = 1, mande:
json
{"titulo": "Estudar FastAPI", "descricao": "Atualizado", "concluida": true, "tags": ["python"]}

Deve dar 200, e repare que data_atualizacao mudou (ficou diferente de data_criacao).

5. Filtrar por situação — GET /tarefas

 Preencha só concluida = true → deve devolver só a tarefa 1 (que você marcou como concluída).

6. Filtrar por tag — GET /tarefas

 Preencha só tag = python → deve devolver as 3 tarefas.
 Troque pra tag = estudos → deve devolver só 1.

7. Filtrar por título — GET /tarefas

 Preencha titulo = python (minúsculo) → deve devolver as tarefas com "Python" no título, mesmo em maiúscula.

8. Ordenar — GET /tarefas

 ordenar_por = titulo, ordem = asc → tarefas em ordem alfabética.
 Troque ordem = desc → ordem invertida.

9. Combinar filtros + ordenação — GET /tarefas

 Preencha ao mesmo tempo: concluida = false, tag = python, ordenar_por = data_criacao, ordem = desc → deve devolver só as pendentes com tag python, da mais nova pra mais antiga.

10. Paginação — GET /tarefas

 pagina = 1, limite = 2 → devolve só 2 tarefas, mas "total" mostra o total real (3).
 pagina = 2, limite = 2 → devolve a tarefa restante.

11. Consulta por período — GET /tarefas

 data_inicio = 2020-01-01, data_fim = 2030-01-01 → deve devolver todas (porque foram criadas hoje, dentro desse intervalo).

12. Excluir — DELETE /tarefas/{id}

 id = 3 → deve dar 204 (sem corpo).
 Depois, GET /tarefas/3 → deve dar 404, confirmando que foi excluída.