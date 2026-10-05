from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
 
from database import criar_tabela, inserir, listar, atualizar, excluir

criar_tabela()

app = FastAPI(title="API Lista de Tarefas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

PASTA = Path(__file__).resolve().parent

class TarefaIn(BaseModel):
    titulo: str
    status: str = "pendente"

@app.get("/tarefas")
def rota_listar():
    return listar()

@app.post("/tarefas", status_code=201)
def rota_criar(dados: TarefaIn):
    try:
        novo_id = inserir(dados.titulo)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    return {"id": novo_id, "titulo": dados.titulo.strip(), "status": "pendente"}

@app.post("/tarefas/{id}")
def att_rota(id: int, dados: TarefaIn):
    try:
        alterou = atualizar(id, dados.titulo, dados.status)
    except ValueError as erro: 
        raise HTTPException(status_code=400, detail=str(erro))

    if not alterou:
        raise HTTPException(status_code=404, detail=str("Tarefa não encontrada"))
    
    return {"id": id, "titulo": dados.titulo.strip(), "status": dados.status}

@app.delete("/tarefa/{id}")
def rota_excluir(id: int):
    if not excluir(id):
        raise HTTPException(status_code=404, detail="Tareda não encontrada")
    return {"mensagem", "Tarefa deletada"}

app.mount("/", StaticFiles(directory=PASTA / "web", html=True), name="web")