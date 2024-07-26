import hashlib

import io

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from biblioteca.forms import LivroForm, UsuarioForm, LoginForm, Usuario, Livro

from django.db.models import Count, Q

from django.contrib.auth.decorators import user_passes_test, login_required

from django.contrib.auth import authenticate, login as auth_login

from django.contrib import messages


def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = hashlib.sha256(usuario.password.encode('utf-8')).hexdigest()
            usuario.is_active = True
            usuario.save()
            messages.success(request, 'Parabéns Usuário registrado com sucesso!.')
            return redirect('login')
        else:
            return render(request, 'biblioteca/registro.html', {'form': form})
    else:
        form = UsuarioForm()
        return render(request, 'biblioteca/registro.html', {'form': form})


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
    return render(request, 'biblioteca/login.html', {'form': form})


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
            livros = Livro.objects.filter(usuario=usuario)

            context = {
                'usuario': usuario,
                'livros': livros,
            }
        return render(request, 'biblioteca/dashboard.html', context)
    else:
        return redirect('login')


def adicionar_livro(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        if request.method == 'POST':
            form = LivroForm(request.POST)
            if form.is_valid():
                livro = form.save(commit=False)
                livro.usuario_id = request.session.get('usuario_id')
                livro.save()
                messages.success(request, f'Livro \'{livro.nome}\' adicionado com sucesso!')
                return redirect('dashboard')
            else:
                return render(request, 'biblioteca/adicionar_livro.html', {'form': form})
        else:
            form = LivroForm()
        return render(request, 'biblioteca/adicionar_livro.html', {'form': form})
    else:
        return redirect('login')


def logout(request):
    request.session.flush()
    response = redirect('login')
    return response


# VIEWS DE ADMIN

def is_admin(user):
    return user.is_authenticated and user.is_admin


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import Usuario

def is_admin(user):
    return user.is_authenticated and user.is_admin

@user_passes_test(is_admin, login_url='/biblioteca/login/')
def listar_usuarios(request):
    if request.user.is_authenticated and request.user.is_admin:
        usuarios = Usuario.objects.filter(is_admin=False).annotate(num_livros=Count('livros'))
        return render(request, 'biblioteca/listar_usuarios.html', {'usuarios': usuarios})
    else:
        messages.error(request, 'Você não tem permissão para acessar essa página.')
        return redirect('dashboard')

@user_passes_test(is_admin)
def desativar_usuario(request, usuario_id):
    try:
        usuario_a_desativar = get_object_or_404(Usuario, id=usuario_id)
        usuario_a_desativar.is_active = False
        usuario_a_desativar.save()
        messages.success(request, f'Usuário {usuario_a_desativar.nome} desativado com sucesso!')
        return redirect('listar_usuarios')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário não encontrado')
        return redirect('listar_usuarios')

@user_passes_test(is_admin)
def reativar_usuario(request, usuario_id):
    try:
        usuario_a_reativar = get_object_or_404(Usuario, id=usuario_id)
        usuario_a_reativar.is_active = True
        usuario_a_reativar.save()
        messages.success(request, f'Usuário {usuario_a_reativar.nome} reativado com sucesso!')
        return redirect('listar_usuarios')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário não encontrado')
        return redirect('listar_usuarios')

@user_passes_test(is_admin)
def excluir_usuario(request, usuario_id):
    try:
        usuario_a_ser_excluido = get_object_or_404(Usuario, id=usuario_id)
        usuario_a_ser_excluido.delete()
        messages.success(request, f'Usuário {usuario_a_ser_excluido.nome} excluído com sucesso!')
        return redirect('listar_usuarios')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário não encontrado')
        return redirect('listar_usuarios')