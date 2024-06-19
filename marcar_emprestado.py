def marcar_livro_como_emprestado(livros):
    if not livros:
        print('Ops Nenhum livro foi adicionado até o momento...')
        return livros

    while True:
        try:
            print("Livros na lista:")
            for i, livro in enumerate(livros, start=1):
                print(f"{i}. {livro['titulo']}")
            indice = int(input('Digite o número do livro correspondente que você deseja marcar como emprestado: '))
            if 1 <= indice <= len(livros):
                livros[indice - 1]['emprestado'] = True
                print(f'Livro "{livros[indice - 1]["titulo"]}" marcado como EMPRESTADO.')
                return livros
            else:
                print('Ops Número do livro inválido... Tente novamente, por favor!')
        except ValueError:
            print('Entrada não permitida. Por favor, digite apenas caracteres numéricos!')
