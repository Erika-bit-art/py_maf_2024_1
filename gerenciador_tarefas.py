from tarefa import Tarefa
from validador_tarefa import ValidadorTarefa

class GerenciadorTarefas:
    def __init__(self):
        self.tarefas = []


    def adicionar_tarefa(self, tarefa):  
        try:
            ValidadorTarefa.validar(tarefa)
            self.tarefas.append(tarefa)  # append é pra adicionar um novo elemento a lista, classe...
            print(f'Tarefa "{tarefa.nome}" adicionada com sucesso!')

        except ValueError as e:
            print(f'Erro ao adicionar tarefa à lista. ERROR: {e}')


    def visualizar_tarefa(self):
        try:
            if len(self.tarefas) == 0:
                raise ValueError ('Ops! Nehuma tarefa foi adicionada até o momento.') # RAISE = ESTOURA O ERRO NAQUELE MOMENTO
            for idx, tarefa in enumerate (self.tarefas):
                print(f' Tarefa {idx + 1}\n {tarefa}')

        except Exception as e:
            print(f'Erro ao visualizar tarefas. ERROR: {e}')


    def pesquisar_tarefas(self, nome):
        try:
            for tarefa in self.tarefas:
                if tarefa.nome == nome:
                    return tarefa
            raise ValueError(f'Tarefa "{nome}" não encontrada.')

        except Exception as e:
            raise ValueError(f'Erro ao pesquisar tarefa. ERROR: {e}')

    def atualizar_tarefa(self, tarefa):
        try:
               ValidadorTarefa.validar(tarefa)
               tarefa_localizada = self.pesquisar_tarefas(tarefa.nome)
               tarefa_localizada.atualizar(tarefa.nome, tarefa.descricao)
               print(f'Tarefa "{tarefa.nome}" atualizada com sucesso!')

        except Exception as e:
               print(f'Erro ao atualizar a lista de tarefas. ERROR: {e}')

    def remover_tarefas(self, nome):
        try:
            tarefa = self.pesquisar_tarefas(nome)
            self.tarefas.remove(tarefa)
            print(f'Tarefa "{tarefa.nome}" removida com sucesso!')
        except Exception as e:
            print(f'Erro ao remover tarefa da lista. ERROR: {e}')




