// A página é servida pela própria API, então o endereço pode ser relativo
const API_URL = "/tarefas";

let tarefas = [];

const lista = document.getElementById("lista");
const form = document.getElementById("form");
const campoTitulo = document.getElementById("titulo");
const aviso = document.getElementById("aviso");
const mensagem = document.getElementById("mensagem");

function avisar(texto, erro = false) {
  mensagem.textContent = texto;
  mensagem.className = erro ? "erro" : "";
  setTimeout(() => { mensagem.textContent = ""; }, 3000);
}

// O SQLite guarda a data em UTC; aqui convertemos para o horário local
function formatarData(texto) {
  if (!texto) return "";
  const data = new Date(texto.replace(" ", "T") + "Z");
  return "Criada em " + data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

// ---------- Comunicação com a API ----------

// Faz a requisição e, se a API devolver erro, lança a mensagem dela
async function pedir(url, opcoes, erroPadrao) {
  const r = await fetch(url, opcoes);
  if (!r.ok) {
    let detalhe = erroPadrao;
    try {
      const json = await r.json();
      if (typeof json.detail === "string") detalhe = json.detail;
    } catch {}
    throw new Error(detalhe);
  }
  return r;
}

// Read  ->  GET /tarefas
async function carregar() {
  try {
    const r = await fetch(API_URL);
    if (!r.ok) throw new Error();
    tarefas = await r.json();
    aviso.style.display = "none";
    mostrar();
  } catch {
    aviso.style.display = "block";
  }
}

// Create  ->  POST /tarefas
async function adicionar(titulo) {
  await pedir(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ titulo, status: "pendente" })
  }, "Erro ao adicionar");
}

// Update  ->  PUT /tarefas/{id}
async function atualizar(id, dados) {
  const tarefa = tarefas.find(t => t.id === id);
  const novo = { titulo: tarefa.titulo, status: tarefa.status, ...dados };

  await pedir(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(novo)
  }, "Erro ao atualizar");
}

// Delete  ->  DELETE /tarefas/{id}
async function excluir(id) {
  await pedir(`${API_URL}/${id}`, { method: "DELETE" }, "Erro ao excluir");
}

// ---------- Tela ----------

function mostrar() {
  lista.innerHTML = "";

  if (tarefas.length === 0) {
    lista.innerHTML = '<p class="vazio">Sem tarefas ainda</p>';
    return;
  }

  tarefas.forEach(t => {
    const feita = t.status === "concluída";
    const li = document.createElement("li");
    if (feita) li.classList.add("concluida");

    const info = document.createElement("div");
    info.className = "info";

    const icone = document.createElement("span");
    icone.className = "icone";
    icone.textContent = feita ? "✅" : "❌";

    const texto = document.createElement("div");
    texto.className = "texto";

    const titulo = document.createElement("span");
    titulo.className = "titulo";
    titulo.textContent = t.titulo;

    const data = document.createElement("span");
    data.className = "data";
    data.textContent = formatarData(t.data_criacao);

    texto.append(titulo, data);
    info.append(icone, texto);

    const acoes = document.createElement("div");
    acoes.className = "acoes";

    if (!feita) {
      const btnOk = document.createElement("button");
      btnOk.className = "btn-ok";
      btnOk.textContent = "Concluir";
      btnOk.onclick = () => executar(() => atualizar(t.id, { status: "concluída" }), "Marcada como concluída");
      acoes.appendChild(btnOk);
    }

    const btnEdit = document.createElement("button");
    btnEdit.className = "btn-edit";
    btnEdit.textContent = "Editar";
    btnEdit.onclick = () => {
      const novoTitulo = prompt("Novo texto da tarefa:", t.titulo);
      if (novoTitulo === null) return;
      if (!novoTitulo.trim()) return avisar("O título não pode ficar vazio", true);
      executar(() => atualizar(t.id, { titulo: novoTitulo.trim() }), "Tarefa atualizada");
    };

    const btnDel = document.createElement("button");
    btnDel.className = "btn-del";
    btnDel.textContent = "Excluir";
    btnDel.onclick = () => {
      if (confirm(`Excluir a tarefa "${t.titulo}"?`)) {
        executar(() => excluir(t.id), "Tarefa deletada");
      }
    };

    acoes.append(btnEdit, btnDel);
    li.append(info, acoes);
    lista.appendChild(li);
  });
}

// Executa uma ação, recarrega a lista e mostra o resultado
async function executar(acao, textoSucesso) {
  try {
    await acao();
    await carregar();
    avisar(textoSucesso);
  } catch (e) {
    avisar(e.message || "Algo deu errado", true);
  }
}

form.addEventListener("submit", e => {
  e.preventDefault();
  const titulo = campoTitulo.value.trim();
  if (!titulo) return avisar("Escreva a tarefa antes de adicionar", true);
  executar(() => adicionar(titulo), `Tarefa '${titulo}' adicionada`);
  campoTitulo.value = "";
});

carregar();