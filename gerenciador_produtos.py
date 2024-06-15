# GESTÃO DE PRODUTOS USANDO POO


from produto import Produto
#    pasta           classe (dentro dessa pasta)
from validador_produtos import ValidadorProduto

class GerenciadorProduto:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, produto):
        try:
            ValidadorProduto.validar(produto)
            self.produtos.append(produto) # append é pra adicionar um novo elemento a lista, classe...
            print(f'Produto "{produto.nome}" adicionado com sucesso!')

        except ValueError as e:
            print(f'Erro ao adicionar o produto: {e}')


    def listar_produtos(self):
        try:
            if len(self.produtos) == 0:
               raise ValueError('Não há produtos cadastrados até o momento.') # "RAISE" ESTOURA O ERRO NAQUELE MOMENTO
            for idx, produto in enumerate(self.produtos):
                print(f'{idx + 1}. {produto}')

        except Exception as e:
             print(f'Erro ao lista produtos: {e}')

    def buscar_produto(self, codigo):
        try:
            for produto in self.produtos:
                if produto.codigo == codigo:
                    return produto
            raise ValueError (f'Produto com código: "{codigo}", não encontrado')
        except Exception as e:
            print(f'Erro ao buscar produto: {e}')

    def remover_produto(self,codigo):
        try:
            produto = self.buscar_produto(codigo)
            self.produtos.remove(produto)
            print(f'Produto "{produto.nome}" removido com sucesso!')

        except Exception as e:
            print(f'Erro ao tentar remover o produto. Erro: {e}')

    def atualizar_produto(self,produto):
        try:
            ValidadorProduto.validar(produto)
            produto_localizado = self.buscar_produto(produto.codigo)
            produto_localizado.atualizar(produto.nome, produto.preco, produto.quantidade)
            print(f'Produto "{produto.nome}" atualizado com sucesso!')

        except Exception as e:
            print(f'Erro ao atualizar a lista de produtos. ERROR: {e}')



