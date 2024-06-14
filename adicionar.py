def adicionar_tarefa(tarefas):
    nome = input('Digite o nome da tarefa: ')
    descricao = input('Por favor, descreva brevemente a tarefa definida: ')

    tarefa = {
        'nome': nome,
        'descricao': descricao,
        'concluida': False
    }

    tarefas.append(tarefa)
    print(f"Tarefa '{nome}' adicionada com sucesso!")

