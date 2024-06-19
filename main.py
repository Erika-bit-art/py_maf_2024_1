from menu import Menu
from gerenciador_tarefas import GerenciadorTarefas
from tarefa import Tarefa


def main():
    gerenciador_tarefas = GerenciadorTarefas()

    while True:
        opcao = Menu.exibir()
        if opcao == 1:
            nome = input('Digite o nome da tarefa: ')
            descricao = input('Descreva os detalhes da tarefa a ser adicionada: ')
            tarefa = Tarefa(nome, descricao)
            gerenciador_tarefas.adicionar_tarefa(tarefa)

        elif opcao == 2:
            gerenciador_tarefas.visualizar_tarefa()

        elif opcao == 3:
            nome = input('Digite o nome da tarefa: ')
            gerenciador_tarefas.pesquisar_tarefas(nome)

        elif opcao == 4:
            nome = input('Digite o nome da tarefa: ')
            descricao = input('Descreva os detalhes da tarefa a ser adicionada: ')
            tarefa = Tarefa(nome, descricao)
            gerenciador_tarefas.atualizar_tarefa(tarefa)

        elif opcao == 5:
            nome = input('Digite o nome da tarefa: ')
            gerenciador_tarefas.remover_tarefas(nome)

        elif opcao == 6:
            print('Saindo... Até a próxima!')
            break

        else:
            print('Opção inválida. Por favor, digite outro número.')



    

if __name__ == '__main__':
    main()



