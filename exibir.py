def exibir_tarefas(tarefas):
    if not tarefas:
        print('Nenhuma tarefa foi adicionada até o momento.')
        return

    for idx, tarefa in enumerate(tarefas):
        status = 'Concluída' if tarefa ['concluida'] else "Não Concluída"
        print('\n Tarefa {}:'.format(idx + 1))
        print('Nome: {}'.format(tarefa["nome"]))
        print('Descrição: {}'.format(tarefa["descricao"]))
        print('status:{}'.format(status))