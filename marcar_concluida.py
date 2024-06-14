def marcar_tarefa_concluida(tarefas):
    if not tarefas:
        print('Nenhuma tarefa foi adicionada até o momento.')
        return tarefas

    try:
        indice = int(input('Digite o número da tarefa para marcá-la como concluída: ')) - 1
        if 0 <= indice < len(tarefas):
            tarefas[indice]['concluida'] = True
            print(f'Tarefa "{tarefas[indice]["nome"]}" marcada com sucesso!')
        else:
            print('Número da tarefa digitado inválido. Por favor, digite outro número.')
    except ValueError:  # tratamento da exceção
        print('Entrada inválida. Por favor, digite um valor numérico.')








