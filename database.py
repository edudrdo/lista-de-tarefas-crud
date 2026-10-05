import sqlite3
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def conectar():
    conexao = sqlite3.connect(DATA_DIR / "banco.db")
    conexao.row_factory = sqlite3.Row   # permite acessar colunas pelo nome
    return conexao

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "titulo" VARCHAR(100) NOT NULL,
            "status" VARCHAR(20) NOT NULL DEFAULT 'pendente',
            "data_criacao" DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conexao.commit()
    conexao.close()

def inserir(titulo):
    titulo = titulo.strip()
    if not titulo:
        raise ValueError("O titulo não pode ficar vazio")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""INSERT INTO tarefas
                    (titulo, status, data_criacao) 
                    VALUES(?, ?, ?) 
                    """, (titulo, "pendente", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    return novo_id

def listar():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                    SELECT id, titulo, status, data_criacao FROM tarefas ORDER BY id
                    """)
    linhas = cursor.fetchall()

    conexao.close()
    return [dict(linha) for linha in linhas]

def atualizar(id, titulo, status):
    titulo = titulo.strip()
    if not titulo:
        raise ValueError("O titulo não pode ficar vazio")
    if status not in ("pendente", "concluida"):
        raise ValueError("Status inválido")
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""UPDATE tarefas
                    SET titulo = ?, status = ? WHERE id = ?
                    """, (titulo, status, id))
    
    conexao.commit()
    alterou = cursor.rowcount > 0
    conexao.close()
    return alterou

def excluir(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""DELETE FROM tarefas WHERE id = ?""",(id,))

    conexao.commit()
    excluiu = cursor.rowcount > 0
    conexao.close()
    return excluiu

if __name__ == "__main__":
    criar_tabela()