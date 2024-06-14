peso = float(input("Digite o seu peso em kg: "))
altura = float(input("Digite a sua altura em metros: "))
imc = peso / (altura ** 2)

print('Seu índice de massa corporal (imc) é {:.2f}'.format(imc))