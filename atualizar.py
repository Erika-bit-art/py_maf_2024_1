def atualizar_contato(contatos):
    if not contatos:
        print('Ops! Nenhum contato foi adicionado até o momento...')
        return

    while True:
        try:
            indice = int(input('Digite o número da lista correspondente ao contato que você deseja atualizar:\n(exemplo: contato 1 --> número: 1 )'))
            if 1 <= indice <= len(contatos):
                contato_atualizar = contatos[indice - 1]
                nome_atualizar = input('Insira o nome do contato a ser atualizado (ou pressione "Enter" para manter o mesmo): ')
                telefone_atualizar = int(input('Insira o novo telefone do contato (ou pressione Enter para manter o mesmo): '))
                email_atualizar = input('Insira o novo email (ou pressione Enter para manter o mesmo): ')

                if nome_atualizar:
                    contato_atualizar['nome'] = nome_atualizar
                if telefone_atualizar:
                    contato_atualizar['telefone'] = telefone_atualizar
                if email_atualizar:
                    contato_atualizar['email'] = email_atualizar

                print(f'Contato de "{contato_atualizar["nome"]}" --> atualizado com sucesso!')
                return
            else:
                print('Ops! número da lista inválido... Tente novamente, por favor!')
        except ValueError:
            print('Entrada não permitida. Por favor, digite apenas caracteres numéricos!')