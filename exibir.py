def exibir_livros(livros):
    if not livros:
        print("Ops Nenhum livro foi adicionado até o momento...")
        return

    for idx, livro in enumerate(livros):
        status = livro.get('emprestado', 'Disponível')
        print('\n Livro {}:'.format(idx + 1))
        print('Título: {}'.format(livro['titulo']))
        print('Autor: {}'.format(livro['autor']))
        print('Ano de Publicação: {}'.format(livro['ano_de_publicacao']))
        print('Status: {}'.format(status))