def calcular_media(alunos):
    if not alunos:
        print('Nenhum aluno(a) cadastrado(a).')
        return

    for aluno in alunos:
        media = (aluno['nota1'] + aluno['nota2']) / 2
        if media >= 6:
            situacao = 'Aprovado(a)'

        elif 4 <= media < 6:
            situacao = 'Recuperação'

        else:
            situacao = 'Reprovado(a)'

        print(f'Aluno: {aluno ["nome"]}')
        print(f'Media: {media:.2f}')
        print(f'Situação: {situacao}')
