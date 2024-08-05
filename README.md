## Olá, meu nome é Érika Fernandes, sou estudante do Senac.

## Bem vindo(a) à documentação do meu projeto final!

O Projeto com nome do arquivo raiz 'Trabalho_Final' é caracterizado como 'Gerenciador de Registros Olímpicos'. 
O objetivo do Gerenciador é permitir ao usuário fã ou interessado nos jogos Olímpicos documentar os momentos mais 
marcantes de qualquer edição do evento olímpico. Momentos que são especiais demais para ficar só na memória. Claro, 
precisam de um registro concreto e facilmente acessível.

Para realizar a instalação do projeto clone o repositório 'https://github.com/Erika-bit-art/py_maf_2024_1.git' 
no Github na Branch 'TRABALHO_FINAL_SENAC_ATUALIZADO'. Selecione o diretório do projeto e execute no terminal:
'python manage.py runserver'. Realize a instalação das dependencias necessárias incluindo: 'pip install django', 
'pip install pillow','pip install itsdangerous' além de executar os comando triviais 'python manage.py makemigrations' 
e o 'python manage.py migrate'.

As funcionalidades da aplicação consistem basicamente no: cadastro, login, acesso a dashboard do usuário, criação do 
registro olímpico pela inserção de campos específicos (atleta, modalidade, país, medalha, ano, local sede, momento, foto),
e eventualmente o logout e mudar senha. Para o admin, é possível: verificar o quantitativo de usuários, sendo os ativos
e os inativos também; listar os usuários, desativar, reativar e reenviar um email de ativação de conta. 

## Em cadastro: 
'def cadastro' 
(Esta view processa o formulário de cadastro de usuários. 
Se o formulário for válido, um novo usuário é criado e redirecionado para a página de login.)

## Em login: 
'def login'
(Esta view processa o formulário de login dos usuários. Se as informações fornecidas forem válidas, o usuário é
autenticado e a sessão é iniciada, redirecionando-o para a dashboard do usuário. Se as credenciais estiverem incorretas, 
exibe uma mensagem de erro e solicita o preenchimento correto do formulário.)

## Em dashboard e criação do registro olímpico:

'def dashboard'
(Esta view exibe a página inicial do painel de controle para usuários autenticados. Fornece as informações 
relevantes para o usuário,como os registros olímpicos inseridos pelo mesmo, renderizando o template do dashboard. 
Se o usuário não estiver autenticado, é redirecionado para a página de login.)

'def adicionar_registro'
(Esta view processa o formulário de adição de registros olímpicos. Se o formulário for válido, 
um novo registro é criado e associado ao usuário atual com os campos correspondentes ao tema.)

'def editar_registro'
(Esta view processa o formulário para editar um registro existente. Se o formulário for válido, as alterações são salvas 
e o usuário é redirecionado para uma página de dashboard com os dados atualizados.)

'def excluir_registro'
(Esta view processa a solicitação para excluir um registro existente. Após a confirmação, o registro é removido do banco 
de dados e o usuário é redirecionado para a dashboard já atualizada sem o registro olímpico em questão.)

## Em logout:

'def logout'
(Esta view encerra a sessão do usuário atual. Após o logout, o usuário é redirecionado para a página de login ou para a 
página inicial do site. A sessão do usuário é encerrada, garantindo que ele não tenha mais acesso às páginas 
protegidas sem reautenticação.)

## Em mudar senha:
'def change_password'
(Esta view redireciona o usuario para página de mudança de senha que senha se validada redireciona o usuário para a sua
dashboard de registros olímpicos exibindo uma mensagem de 'success' se a senha for alterada. O contrário também se aplica)

## Para admin:
'def excluir_usuario', 'def desativar_usuario', 'def reativar_usuario'
(Estas views permitem ao usuario definido como admin= true modificarem as configurações do sistema. Se valiadas, é possível
que o admin exclua, desative ou reative algum usuário)

## Outros:
'def send_activation_email', 'def resend_activation_email', 'def activate'
(Estas views possibilitam a confirmação de cadastro do usuário via uma notificação via email ou ainda mesmo que o admin
reenvie um email para algum usuário)

O Projeto Final 'Gerenciador de Registros Olímpicos' conta ainda com modelagens nas files Forms (com LoginForm, Registro
Form, Change Password, entre outros) e com estruturações na file Models onde são definidos os objetos a serem trabalhados
o cerne de toda a aplicação.

Na modelagem estética são caracterizados os HTMLS de:
(adicionar_registro, dashboard, editar_registro, excluir_registro para REGISTROS)
(activation_email, cadastro, change_password, listar_usuarios, login para USUARIOS)

OBS: os HTMLS: 'dashboard' e 'base' são os grandes alicerces do projeto.

A citar ainda as files de 'urls' com os direcionamentos de caminhos das views e htmls.

A file 'settings' padrão na criação do projeto é configurada automaticamente com algumas eventuais adições manuais como
o nome da aplicação, caminhos, e ativação de email, por exemplo.

O projeto tem ainda outras dependências geradas por default logo na criação do mesmo via terminal.

## Requisitos do Sistema:

Python no mínimo =2.2.9
Pip install Django
Pip install Pillow
Pip install itsdangerous

## CONTRIBUIÇÃO: 
projeto desenvolvido com base nas aulas do curso realizado, pesquisas em fontes diversas e conhecimento gerais.

## OBS: 
A considerar que o projeto foi desenvolvido por uma estudante em iniciação, eventuais erros de funcionamento podem ocorrer. 
A destacar a autenticação de senha do usuario recém criado e também o envio do email de confirmação de ativação de conta.
Por isso, para a usabilidade da aplicação ser completa, excepcionalmente, forneco o email e senha de usuários registrados 
no banco de dados que estão sendo validados corretamente, visto que são usuários representativos ('ficcionais'). 
São eles:

erika@gmail.com
senha: e1234@

billie@gmail.com
senha: bb1234@ 

henrique@gmail.com
senha: h1234@

## BPM DO PROJETO
https://drive.google.com/file/d/1TCcNkHmxSPWe873y9KFgyPwt-ipIrUyY/view

É isso! Muito Obrigada!

Todos os Direitos Reservados.







