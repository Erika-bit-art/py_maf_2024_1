from menu import Menu # GESTÃO DE PRODUTOS USANDO POO
from gerenciador_produtos import GerenciadorProduto
from produto import Produto

def main():
    gerenciador_produtos = GerenciadorProduto()
    while True:
        opcao = Menu.exibir()
        if opcao == '1':
            codigo = input('Digite o código do produto: ')
            nome = input('Digite o nome do produto: ')
            preco = float(input('Digite o preço do produto: '))
            quantidade = int(input('Digite a quantidade do produto:'))
            produto = Produto(codigo, nome, preco, quantidade)
            gerenciador_produtos.adicionar_produto(produto)
        elif opcao == '2':
            gerenciador_produtos.listar_produtos()

        elif opcao == '3':
            codigo = input('Digite o código do produto: ')
            nome = input('Digite o nome do produto: ')
            preco = float(input('Digite o preço do produto: '))
            quantidade = int(input('Digite a quantidade do produto:'))
            produto = Produto(codigo, nome, preco, quantidade)
            gerenciador_produtos.atualizar_produto(produto)


        elif opcao == '4':
            codigo = input('Digite o código do produto a excluir:')
            gerenciador_produtos.remover_produto(codigo)

        elif opcao == '5':
            print('Saindo...')
            break

        else:
           print('Opção inválida. Por favor, digite outro número.')



if __name__ == '__main__':
    main()