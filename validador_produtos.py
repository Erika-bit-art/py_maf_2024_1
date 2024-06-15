# GESTÃO DE PRODUTOS USANDO POO
class ValidadorProduto:
        @staticmethod
        def validar(produto):
            if produto is None:
                raise ValueError('Produto não pode ser nulo')
            if produto.codigo is 0:
                raise ValueError('Código de produto não pode ser nulo')
            if produto.nome == '':
                raise ValueError('Nome do produto não pode ser vazio')
            if produto.preco <= 0:
                raise ValueError('Valor do produto deve ser maior que zero')
            if produto.quantidade <= 0:
                raise ValueError('Quantidade do produto dever ser maior que zero')

