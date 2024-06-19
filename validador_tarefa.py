class ValidadorTarefa:

    @staticmethod
    def validar(tarefa):

        if tarefa.nome == '':
            raise ValueError ('ERROR: O nome da tarefa não pode ser vazio')

        if tarefa.descricao == '':
            raise ValueError ('ERROR: A descrição da tarefa não pode ser vazia')


