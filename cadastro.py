def cadastrar_aluno(alunos):
    nome = input('Digite o nome do aluno(a): ')
    idade = input('Digite a idade do aluno(a): ')
    cidade = input('Digite a cidade do aluno(a): ')
    nota1 = float(input('Digite a nota 1 do aluno(a): '))
    nota2 = float(input('Digite a nota 2 do aluno(a): '))

    aluno = {
        "nome": nome,
        "idade": idade,
        "cidade": cidade,
        "nota1": nota1,
        "nota2": nota2, }

    alunos.append(aluno)
    print(f'Aluno(a) {nome} cadastrado com sucesso!')
