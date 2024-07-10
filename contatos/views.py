import hashlib

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import Usuario, Contato
from .forms import UsuarioForm, ContatoForm, LoginForm, PasswordChangeForm
from django.db.models import Count, Q

from django.contrib.auth.decorators import user_passes_test, login_required

from django.contrib.auth import authenticate, login as auth_login

from django.contrib import messages

from .token_utils import generate_token


# views para admin
#def is_admin(user):
#    return user.is_authenticated and user.is_admin


#@login_required
#@user_passes_test(is_admin)


#@login_required
#@user_passes_test(is_admin)

def resend_activation_email(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    if usuario:
        send_activation_email(request, usuario)
        return True


def send_activation_email(request, usuario):
    token = generate_token(usuario.pk)
    current_site = get_current_site(request)
    mail_subject = 'Ative sua conta'
    message = render_to_string('usuarios/activation_email.html', {

        'user': usuario,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(usuario)),
        'token': token,
    })
    send_mail(mail_subject, message, 'erika.fernandes@gmail.com',[usuario.email], fail_silently=False)


def desativar_usuario(request, usuario_id):
    try:
        #usuario_logado = request.user
        usuario_logado_id = request.session.get('usuario_id')
        usuario_logado = Usuario.objects.get(id=usuario_logado_id)
        if usuario_logado:
            usuario_a_desativar = get_object_or_404(Usuario, id=usuario_id)
            if usuario_logado.is_admin:
                usuario_a_desativar.is_active = False
                usuario_a_desativar.save()
                messages.success(request, f'Usuário \'{usuario_a_desativar.nome}\' desativado com sucesso.')
            else:
                messages.error(request, 'Você não tem permissão para desativar usuários.')
                return redirect('dashboard')
            return redirect('listar_usuarios')
        else:
            return redirect('login')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')


def listar_usuarios(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.is_admin:

            query = request.GET.get('q')
            status = request.GET.get('status')
            idade = request.GET.get('idade')
            usuarios = Usuario.objects.all()

            if query:
                usuarios = usuarios.filter(Q(nome__icontains=query) | Q(email__icontains=query))

            if status:
                is_active = True if status == 'ativo' else False
                usuarios = usuarios.filter(is_active=is_active)
            else:
                usuarios = usuarios.all()  # Retorna todos os usuários, independentemente do status

            if idade:
                try:
                    idade = int(idade)
                    faixa_min = idade - 3
                    faixa_max = idade + 3
                    usuarios = usuarios.filter(idade__range=(faixa_min, faixa_max))
                except ValueError:
                    pass  # se a idade não for um número, ele vai ignorar (pass)

            usuarios = usuarios.filter(is_admin=False).annotate(num_contatos=Count('contatos'))
            return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})
        else:
            messages.error(request, 'Você não tem permissão para acessar essa página.')
            return redirect('dashboard')
    else:
        return redirect('login')


#@login_required
#@user_passes_test(is_admin)
def reativar_usuario(request, usuario_id):
    try:
        #usuario_logado = request.user
        usuario_logado_id = request.session.get('usuario_id')
        usuario_logado = Usuario.objects.get(id=usuario_logado_id)
        if usuario_logado:
            usuario_a_reativar = get_object_or_404(Usuario, id=usuario_id)
            if usuario_logado.is_admin:
                usuario_a_reativar.is_active = True
                usuario_a_reativar.save()
                messages.success(request, f'Usuário \'{usuario_a_reativar.nome}\' reativado com sucesso.')
            else:
                messages.error(request, 'Você não tem permissão para reativar usuários.', extra_tags='danger')
                return redirect('dashboard')
            return redirect('listar_usuarios')
        else:
            return redirect('login')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')


#@login_required
#@user_passes_test(is_admin)
def excluir_usuario(request, usuario_id):
    #usuario_logado = request.user
    usuario_logado_id = request.session.get('usuario_id')
    usuario_logado = Usuario.objects.get(id=usuario_logado_id)
    if usuario_logado:
        usuario_a_ser_excluido = get_object_or_404(Usuario, id=usuario_id)
        if usuario_logado.is_admin:
            usuario_a_ser_excluido.delete()
            messages.success(request, f'Usuário \'{usuario_a_ser_excluido.nome}\' excluído com sucesso.')
        else:
            messages.error(request, 'Você não tem permissão para excluir usuários.')
        return redirect('listar_usuarios')
    else:
        return redirect('login')


# views para não admins
def adicionar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.senha = hashlib.sha256(usuario.senha.encode('utf-8')).hexdigest()
            usuario.save()
            send_activation_email(request, usuario)
            messages.success(request, 'Por favor, verifique o seu e-mail para ativar a sua conta.')
            return redirect('login')
        else:
            return render(request, 'usuarios/adicionar_usuario.html', {'form': form})
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/adicionar_usuario.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.defer('senha').get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Conta ativada com sucesso. Você já pode fazer login agora.')
        return redirect('login')
    else:
        messages.error(request, 'Link de ativação expirado.')
        return redirect('registro')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            hashed_password = hashlib.sha256(senha.encode('utf-8')).hexdigest()

            try:
                usuario = Usuario.objects.get(email=email, senha=hashed_password)
                # usuario = authenticate(request, username=email, password=hashed_password)
                if usuario is not None:
                    if usuario.is_active:
                        request.session['usuario_id'] = usuario.id
                        # auth_login(request, usuario)
                        return redirect('dashboard')
                    else:
                        form.add_error(None, 'Este usuário está desativado.')
            except Usuario.DoesNotExist:
                form.add_error(None, 'Email ou senha incorretos.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


def adicionar_contato(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        if request.method == 'POST':
            form = ContatoForm(request.POST)
            if form.is_valid():
                contato = form.save(commit=False)
                contato.usuario_id = request.session.get('usuario_id')
                contato.save()
                messages.success(request, f'Contato \'{contato.nome}\' adicionado com sucesso!')
                return redirect('dashboard')
            else:
                return render(request, 'contatos/adicionar_contato.html', {'form': form})
        else:
            form = ContatoForm()
        return render(request, 'contatos/adicionar_contato.html', {'form': form})
    else:
        return redirect('login')


def editar_contato(request, contato_id):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        contato = get_object_or_404(Contato, id=contato_id, usuario_id=usuario_id)
        if request.method == 'POST':
            form = ContatoForm(request.POST, instance=contato)
            if form.is_valid():
                form.save()
                messages.success(request, f'Contato \'{contato.nome}\' atualizado com sucesso!')
                return redirect('dashboard')

        form = ContatoForm(instance=contato)
        return render(request, 'contatos/editar_contato.html', {'form': form, 'contato': contato})
    else:
        return redirect('login')


def excluir_contato(request, contato_id):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        contato = get_object_or_404(Contato, id=contato_id, usuario_id=usuario_id)
        if request.method == 'POST':
            contato.delete()
            messages.success(request, f'Contato excluído com sucesso!')
            return redirect('dashboard')
        return render(request, 'contatos/excluir_contato.html', {'contato': contato})
    else:
        return redirect('login')


def dashboard(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        query = request.GET.get('q')
        usuario = Usuario.objects.defer('senha').get(
            id=usuario_id)  # defer() carrega todos os campos do modelo, exceto o(s) especificado(s)
        contatos = Contato.objects.filter(usuario=usuario)

        if query:
            contatos = contatos.filter(
                Q(nome__icontains=query) |
                Q(email__icontains=query) |
                Q(bairro__icontains=query) |
                Q(cidade__icontains=query) |
                Q(uf__icontains=query)
            )

        return render(request, 'contatos/dashboard.html', {'usuario': usuario, 'contatos': contatos})
    else:
        return redirect('login')

def logout(request):
    request.session.flush()
    return redirect('login')


def change_password(request):  # TÁ COM ERRO, PROF VAI VER O Q É
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.only('email').get(id=usuario_id)  # only expoe só o email, oculta os outros(senha..)
        if request.method == 'POST':
            form = PasswordChangeForm(request.POST)
            if form.is_valid():  # se validou no def clean la no forms, é isso q essa parte faz
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['new_password']

                if Usuario.get(email=usuario.email, senha=hashlib.sha256(old_password.encode('utf-8')).hexdigest()):
                    usuario.senha = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
                    usuario.save()
                    messages.success(request, 'Senha alterada com sucesso!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'A senha antiga está incorreta', extra_tags='danger')
            else:
                messages.error(request, 'Por favor, corrija os erros', extra_tags='danger')

        else:
            form = PasswordChangeForm()

        return render(request, 'usuarios/change_password.html', {'form': form})
    else:
        return redirect('login')
