def adicionar_livro(livros):
 print('Vamos adicionar um livro?')
 titulo = input('Digite o nome do livro: ')
 autor = input('Digite o autor: ')
 ano_de_publicacao = input('Qual é o ano de pulicação do livro: ')
 status = input('O livro está disponível ou foi emprestado?: ')  # talvez tenha que tirar

 livro ={   # o nome "livro" tem que bater com o que tá em aspas na linha 15, por isso, não "livroS"

      'titulo': titulo,
       'autor': autor,
       'ano_de_publicacao': ano_de_publicacao,
       'status': False}

 livros.append(livro)
 print(f'O livro: {titulo}. Foi adicionado com sucesso!')
