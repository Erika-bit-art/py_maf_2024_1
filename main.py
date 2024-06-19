from menu import menu
from adicionar import adicionar_contato
from remover import remover_contato
from visualizar import visualizar_contatos
from atualizar import atualizar_contato

def main():
    contatos = []
    while True:
        escolha = menu()
        if escolha == '1':
            adicionar_contato(contatos)

        elif escolha == '2':
             visualizar_contatos(contatos)

        elif escolha == '3':
          atualizar_contato(contatos)
        elif escolha == '4':
            remover_contato(contatos)

        else:
            print('Número inválido. Por favor, tente novamente.')




if __name__ == '__main__':
        main()








