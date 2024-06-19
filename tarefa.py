class Tarefa:

    # ATRIBUTOS

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
        

    def __str__(self):
        return f'Nome: {self.nome} \nDescrição: {self.descricao}'


    # MÉTODOS (AÇÕES)


    def atualizar(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
