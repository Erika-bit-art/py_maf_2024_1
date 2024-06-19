def adicionar_contato(contatos):
 print('Quer adicionar um contato?Vamos lá!')
 nome = input('Digite o nome do contato: ')
 telefone = int(input('Insira o número a ser adicionado (SEM hífens ou parênteses): '))
 email = input('Digite o email do contato correspondente: ')


 contato ={   # o nome "contato" tem que bater com o que tá em aspas na linha 15, por isso, não "contatoS"

      'nome': nome,
       'telefone': telefone,
       'email': email, }

 contatos.append(contato)
 print(f'O contato de "{nome}" Foi adicionado com sucesso!')