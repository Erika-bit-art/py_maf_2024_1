from menu import menu
from adicionar import adicionar_livro
from exibir import exibir_livros
from marcar_emprestado import marcar_livro_como_emprestado
from remover import remover_livro
from pesquisar import pesquisa_livros


def main():
    livros = []
    while True:
        escolha = menu()
        if escolha == '1':
            adicionar_livro(livros)

        elif escolha == '2':
             exibir_livros(livros)

        elif escolha == '3':
            marcar_livro_como_emprestado(livros)
        elif escolha == '4':
            remover_livro(livros)

        elif escolha == '5':
            pesquisa_livros(livros)

        elif escolha == '6':
            print('Fechando o programa... até a próxima!')
            break

        else:
            print('Número inválido. Por favor, tente novamente.')

if __name__ == '__main__':
    main()
