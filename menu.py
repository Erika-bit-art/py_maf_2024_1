class Menu:

    @staticmethod
    def exibir():
        print('\nMenu Principal\nSeja bem-vindo(a) ao Sistema de Gerenciamento de Tarefas.\nAqui, você pode organizar as suas tarefas pendentes ou completas de forma prática e funcional.\nVamos começar?\Escolha a opção desejada:')
        print('1. Adicionar tarefa')
        print('2. Visualizar tarefas adicionadas')
        print('3. Pesquisar uma tarefa')
        print('4. Atualizar o status de uma tarefa (pendente ou concluída)')
        print('5. Remover uma tarefa da lista')
        print('6. Fechar o programa')

        opcao = int(input('Escolha a opção desejada: '))
        return opcao