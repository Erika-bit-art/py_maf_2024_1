# GESTÃO DE PRODUTOS USANDO POO


class Produto:

    # ATRIBUTOS
    def __init__(self, codigo, nome, preco, quantidade):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def __str__(self):
        return f'Código:{self.codigo}, Nome: {self.nome}, Preço: R${self.preco:.2f}, Quantidade: {self.quantidade}'

    # MÉTODOS (AÇÕES)????????

    def atualizar(self, nome, preco, quantidade):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
