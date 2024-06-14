def exibir_alunos(alunos):
    if not alunos:
        print('Nenhum aluno cadastrado...')
        return

    for idx, aluno in enumerate(alunos):
        print(f'\nAluno {idx + 1}.')
        print(f'Nome: {aluno["nome"]}')
        print(f'Idade: {aluno["idade"]}')
        print(f'Cidade: {aluno["cidade"]}')
        print(f'Nota 1: {aluno["nota1"]}')
        print(f'Nota 2: {aluno["nota2"]}')