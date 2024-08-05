import base64
import io
from PIL import Image
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from .models import Usuario, Registro
from .forms import UsuarioForm, RegistroForm, LoginForm, PasswordChangeForm

from django.db.models import Count, Q
from django.utils.encoding import force_str
from django.contrib import messages

from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import hashlib

from .token_utils import generate_token


def cadastro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = hashlib.sha256(usuario.password.encode('utf-8')).hexdigest()
            usuario.is_active = True
            usuario.save()
            messages.success(request, 'Parabéns usuário registrado com sucesso!')
            return redirect('login')
        else:
            return render(request, 'usuarios/cadastro.html', {'form': form})
    else:
        form = UsuarioForm()
        return render(request, 'usuarios/cadastro.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            try:
                usuario = Usuario.objects.get(email=email, password=hashed_password)

                if usuario is not None:
                    if usuario.is_active:
                        request.session['usuario_id'] = usuario.id

                        return redirect('dashboard')
                    else:
                        form.add_error(None, 'Este usuário está desativado.')
            except Usuario.DoesNotExist:
                form.add_error(None, 'Email ou senha incorretos :(')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


def dashboard(request):
    nome = request.session.get('nome_usuario', 'visitante')
    usuario_id = request.session.get('usuario_id')

    if usuario_id:
        usuario = Usuario.objects.defer('password').get(id=usuario_id)
        if usuario.is_admin:
            total_usuarios = Usuario.objects.filter(is_admin=False).count()
            usuarios_ativos = Usuario.objects.filter(is_admin=False, is_active=True).count()
            usuarios_inativos = total_usuarios - usuarios_ativos
            ultimos_usuarios = Usuario.objects.filter(is_admin=False).order_by('-created_at')[:5]

            context = {
                'usuario': usuario,
                'total_usuarios': total_usuarios,
                'usuarios_ativos': usuarios_ativos,
                'usuarios_inativos': usuarios_inativos,
                'ultimos_usuarios': ultimos_usuarios
            }
        else:
            registros = Registro.objects.filter(usuario=usuario)

            context = {
                'usuario': usuario,
                'registros': registros,
            }
        return render(request, 'registros/dashboard.html', context)
    else:
        return redirect('login')


def logout(request):
    request.session.flush()
    response = redirect('login')
    return response


def send_activation_email(request, usuario):
    token = generate_token(usuario.pk)
    current_site = get_current_site(request)
    mail_subject = 'Ative sua conta'
    from_email = 'erika.fernandes1409@gmail.com'
    recipient_list = [usuario.email]
    message = render_to_string('usuarios/activation_email.html', {
        'user': usuario,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(usuario)),
        'token': token,
    })
    send_mail(mail_subject, message, 'erika.fernandes1409@gmail.com', [usuario.email], fail_silently=False)


def change_password(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.only('email').get(id=usuario_id)
        if request.method == 'POST':
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['new_password']

                if Usuario.objects.get(email=usuario.email,
                                       password=hashlib.sha256(old_password.encode('utf-8')).hexdigest()):
                    usuario.password = hashlib.sha256(new_password.encode('utf8')).hexdigest()
                    usuario.save()
                    messages.success(request, 'Senha alterada com sucesso!')
                    return redirect('dashboard')
                else:
                    messages.error('old_password', 'Senha antiga inválida.', extra_tags='danger')
        else:
            form = PasswordChangeForm()
        return render(request, 'usuarios/change_password.html', {'form': form})
    else:
        return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.defer('password').get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Conta ativada com sucesso! Agora você pode fazer login.')
        return redirect('login')
    else:
        messages.error(request, 'Link de ativação inválido.')
        return render('registro')


def adicionar_registro(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        if request.method == 'POST':
            form = RegistroForm(request.POST, request.FILES)
            if form.is_valid():
                registro = form.save(commit=False)
                registro.usuario_id = request.session.get('usuario_id')

                if 'foto' in request.FILES:
                    imagem = Image.open(request.FILES['foto'])
                    imagem = imagem.resize((300, 300), Image.LANCZOS)
                    buffered = io.BytesIO()
                    imagem.save(buffered, format="PNG")
                    registro.foto_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

                registro.save()
                messages.success(request, f'Registro \'{registro.atleta}\' adicionado com sucesso!')
                return redirect('dashboard')
            else:
                return render(request, 'registros/adicionar_registro.html', {'form': form})
        else:
            form = RegistroForm()
        return render(request, 'registros/adicionar_registro.html', {'form': form})
    else:
        return redirect('login')


def editar_registro(request, registro_id):
    registro = get_object_or_404(Registro, id=registro_id, usuario_id=request.session.get('usuario_id'))
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES, instance=registro)
        if form.is_valid():
            registro = form.save(commit=False)

            if 'foto' in request.FILES:
                imagem = Image.open(request.FILES['foto'])
                imagem = imagem.resize((300, 300), Image.LANCZOS)
                buffered = io.BytesIO()
                imagem.save(buffered, format="PNG")
                registro.foto_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            registro.save()
            messages.success(request, f'Registro\'{registro.atleta}\' atualizado com sucesso!')
            return redirect('dashboard')
    else:
        form = RegistroForm(instance=registro)
    return render(request, 'registros/editar_registro.html', {'form': form, 'registro': registro})


def excluir_registro(request, registro_id):
    registro = get_object_or_404(Registro, id=registro_id, usuario_id=request.session.get('usuario_id'))
    if request.method == 'POST':
        registro.delete()
        messages.success(request, f'Registro excluído com sucesso!')
        return redirect('dashboard')
    return render(request, 'registros/excluir_registro.html', {'registro': registro})



from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import Usuario

def is_admin(user):
    return user.is_authenticated and user.is_admin


def listar_usuarios(request):
    query = request.GET.get('q')
    status = request.GET.get('status')
    idade = request.GET.get('idade')
    usuarios = Usuario.objects.all()

    if query:
        usuarios = usuarios.filter(Q(nome__icontains=query) | Q(email__icontains=query))

    if status:
        is_active = True if status == 'ativo' else False
        usuarios = usuarios.filter(is_active=is_active)

    if idade:
        try:
            idade = int(idade)
            faixa_min = idade - 3
            faixa_max = idade + 3
            usuarios = usuarios.filter(idade__range=(faixa_min, faixa_max))

        except ValueError:
            pass

    usuarios = usuarios.filter(is_admin=False).annotate(registros_count=Count('registros'))
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})


def desativar_usuario(request, usuario_id):
    try:
        usuario_a_desativar = get_object_or_404(Usuario, id=usuario_id)
        usuario_a_desativar.is_active = False
        usuario_a_desativar.save()
        messages.success(request, f'Usuário(a) {usuario_a_desativar.nome} desativado com sucesso!')
        return redirect('listar_usuarios')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário(a) não encontrado')
        return redirect('listar_usuarios')


def reativar_usuario(request, usuario_id):
    try:
        usuario_a_reativar = get_object_or_404(Usuario, id=usuario_id)
        usuario_a_reativar.is_active = True
        usuario_a_reativar.save()
        messages.success(request, f'Usuário(a) {usuario_a_reativar.nome} reativado com sucesso!')
        return redirect('listar_usuarios')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário(a) não encontrado')
        return redirect('listar_usuarios')


def excluir_usuario(request, usuario_id):
    try:
        usuario = get_object_or_404(Usuario, id=usuario_id)
        usuario.delete()
        messages.success(request, f'Usuário \'{usuario.nome}\' excluído com sucesso.')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
    return redirect('listar_usuarios')


def resend_activation_email(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    if usuario:
        if not usuario.is_active:
            send_activation_email(request, usuario)
            messages.success(request, 'O e-mail de ativação foi reenviado.')
        else:
            messages.info(request, 'Este usuário já está ativo.')
    return redirect('dashboard')


