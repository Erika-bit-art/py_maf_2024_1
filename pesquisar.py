def pesquisa_livros(livros):
    if not livros:
        print('Ops! Nenhum livro foi adicionado até o momento :(')
        return

    while True:
        try:
            pesquisa = input('Digite o título ou autor do livro que você deseja pesquisar: ')
            for livro in livros:
                if pesquisa.lower() in livro['titulo'].lower() or pesquisa.lower() in livro['autor'].lower():
                    print(f'Título: {livro["titulo"]}, Autor: {livro["autor"]}')
            if not any(pesquisa.lower() in livro['titulo'].lower() or pesquisa.lower() in livro['autor'].lower() for livro in livros):
                print('Livro não encontrado.')
            break
        except ValueError:
            print('Entrada não permitida. Por favor, digite apenas caracteres alfabéticos.')