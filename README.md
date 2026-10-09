# Lista de Tarefas (CRUD)

Aplicação web para gerenciar tarefas, com operações completas de **C**riar, **L**er, **A**tualizar e **E**xcluir (CRUD). O backend é uma API REST em Python com FastAPI, os dados ficam em um banco SQLite e a interface roda no navegador em HTML, CSS e JavaScript.

Projeto desenvolvido para a faculdade.

## Funcionalidades

- Adicionar uma tarefa
- Listar as tarefas, com status e data de criação
- Marcar uma tarefa como concluída
- Editar o título de uma tarefa
- Excluir uma tarefa
- Validação dos dados e mensagens de erro na tela

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python + FastAPI |
| Banco de dados | SQLite (módulo `sqlite3` do Python) |
| Frontend | HTML, CSS e JavaScript |

## Estrutura do projeto

```
lista-de-tarefas-crud/
├── data/              Banco SQLite (criado automaticamente, fora do git)
├── web/
│   ├── index.html     Estrutura da página
│   ├── style.css      Estilo
│   └── script.js      Lógica da interface e chamadas à API
├── database.py        Conexão e operações no banco
├── main.py            API REST (rotas)
├── lista.py           Versão inicial em terminal (lista em memória)
├── requirements.txt   Dependências
└── README.md
```

## Como executar

Pré-requisito: Python 3.10 ou superior.

1. Clone o repositório e entre na pasta:
   ```bash
   git clone https://github.com/edudrdo/lista-de-tarefas-crud.git
   cd lista-de-tarefas-crud
   ```

2. Crie e ative um ambiente virtual:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
   No Linux ou macOS, use `source .venv/bin/activate`. No PowerShell do Windows, se a ativação for bloqueada, rode antes `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Inicie o servidor:
   ```bash
   python -m uvicorn main:app --reload
   ```

5. Abra no navegador:
   - Aplicação: http://localhost:8000
   - Documentação interativa da API: http://localhost:8000/docs

O banco de dados (`data/banco.db`) e a tabela `tarefas` são criados automaticamente na primeira execução.

## API

| Operação | Método | Rota | Corpo da requisição | Respostas |
|---|---|---|---|---|
| Listar tarefas | GET | `/tarefas` | | 200 |
| Criar tarefa | POST | `/tarefas` | `{"titulo": "Estudar"}` | 201, 400 |
| Atualizar tarefa | PUT | `/tarefas/{id}` | `{"titulo": "Estudar", "status": "concluída"}` | 200, 400, 404 |
| Excluir tarefa | DELETE | `/tarefas/{id}` | | 200, 404 |

O campo `status` aceita `pendente` ou `concluída`. Toda tarefa nova começa como `pendente`.

Exemplo de resposta do `GET /tarefas`:

```json
[
  {
    "id": 1,
    "titulo": "Estudar para a prova",
    "status": "pendente",
    "data_criacao": "2026-10-09 17:45:12"
  }
]
```

## Banco de dados

Tabela `tarefas`:

| Campo | Tipo | Observação |
|---|---|---|
| `id` | INTEGER | Chave primária, autoincremento |
| `titulo` | VARCHAR(100) | Obrigatório |
| `status` | VARCHAR(20) | Padrão `pendente` |
| `data_criacao` | DATETIME | Preenchida automaticamente (UTC) |

## Arquitetura

O sistema é dividido em três contêineres: a aplicação web (navegador), a API (FastAPI) e o banco (SQLite).

## Licença

Consulte o arquivo [LICENSE](LICENSE).
