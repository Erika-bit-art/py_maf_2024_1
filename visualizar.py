def visualizar_contatos(contatos):
    if not contatos:
        print("Ops! Nenhum contato foi adicionado até o momento...")
        return

    for idx, contato in enumerate(contatos):
        print('\n Contato {}:'.format(idx + 1))
        print('Nome: {}'.format(contato['nome']))
        print('Telefone: {}'.format(contato['telefone']))
        print('Email: {}'.format(contato['email']))

