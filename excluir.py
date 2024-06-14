def excluir_tarefa(tarefas):
    if not tarefas:
        print('Nenhuma tarefa foi adicionada até o momento')
        return

    try:
        indice = int(input('Digite o número da tarefa que você quer excluir da lista: '))
        if 0 <= indice < len(tarefas):
            tarefa_excluida = tarefas.pop(indice)
            print(f'Tarefa "{tarefa_excluida["nome"]}" excluida com sucesso!')

        else:
         print('Número de tarefa inválido. Por favor, tente novamente.')

    except ValueError:
        print('Entrada inválida. Por favor, digite um valor numérico.')






