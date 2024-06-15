# GESTÃO DE PRODUTOS USANDO POO
class Menu:
    @staticmethod  #comum a todas as instancias(objetos)

    def menu():
        print('\nMenu Principal')
        print('1. Adicionar Produtos')
        print('2. Exibir Produtos')
        print('3. Atualizar Produtos')
        print('4. Excluir Produto')
        print('5. Sair')

        escolha = input ("Ecolha uma das opções acima: ")
        return escolha