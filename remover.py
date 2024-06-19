def remover_livro(livros):
    if not livros:
        print('Ops! Nenhum livro foi adicionado até o momento :(')
        return

    while True:
        try:
            indice = int(input('Digite o número correspondente ao livro que você deseja remover da lista: '))
            if 1 <= indice <= len(livros):
                livro_removido = livros.pop(indice - 1)
                print(f'Livro: "{livro_removido["titulo"]}" --> removido com sucesso!')
                return
            else:
                print('Ops Número do livro inválido... Tente novamente, por favor!')
        except ValueError:
            print('Entrada não permitida. Por favor, digite apenas caracteres numéricos!')
