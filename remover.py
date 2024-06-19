def remover_contato(contatos):
    if not contatos:
        print('Ops! Nenhum livro foi adicionado até o momento :(')
        return

    while True:
        try:
            indice = int(input('Digite o número da lista correspondente ao contato que você deseja remover:\n(exemplo: contato 1 --> número: 1 '))
            if 1 <= indice <= len(contatos):
                contato_removido = contatos.pop(indice - 1)
                print(f'Contato de "{contato_removido["nome"]}" --> removido com sucesso!')
                return
            else:
                print('Ops número da lista inválido... Tente novamente, por favor!')
        except ValueError:
            print('Entrada não permitida. Por favor, digite apenas caracteres numéricos!')
