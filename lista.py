tasks = []

def menu():
    print("\n LISTA DE TAREFAS")
    print("1. Adicionar tarefa")
    print("2. Ver tarefa")
    print("3. Marcar tarefa como feita")
    print("4. Excluir Tarefa")
    print("5. Sair")

def add_task():
    task  = input("Escreva a tarefa: ")
    tasks.append({"task":task, "done":False}) #append - add um elemento no final de uma lista existente
    print(f"Tarefa '{task}' adicionada")

def view_task():
    if not tasks:
        print("Sem tarefas ainda")
        return
    print("\n Suas tarefas:")
    for index, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "❌"
        print(f"{index}. {task['task']} [{status}]")

def completa():
    view_task()
    if not tasks:
        return
    try:
        index = int(input("Escolha o numero da tarefa para ser concluida: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["done"] = True
            print("Marcada como concluida")
        else:
            print("Numero errado")
    except ValueError:
        print("Escolha um numero certo")

def del_task():
    view_task()
    if not tasks:
        return
    try:
        index = int(input("Escolha o numero da tarefa para ser excluida: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            print(f"Tarefa deletada: {removed['task']}")
        else:
            print("Numero errado")
    except ValueError:
        print("Escolha um numero certo")

while True:
    menu()
    choice = input("Escolha um numero entre 1 - 5:")

    if choice == '1':
        add_task()
    elif choice == '2':
        view_task()
    elif choice == '3':
        completa()
    elif choice == '4':
        del_task()
    elif choice == '5':
        print("Tchauuuu")
        break
    else:
        print("Escolah invalida. Tente novamente")