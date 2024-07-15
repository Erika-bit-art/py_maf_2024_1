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
            messages.success(request, 'Parabéns! Usuário registrado com sucesso!.')
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

                        return redirect('personalizar')
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
    cor_preferida = request.COOKIES.get('cor_preferida', 'default')

    if usuario_id:
        usuario = Usuario.objects.defer('password').get(
            id=usuario_id)
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
        return render(request, 'biblioteca/dashboard.html', {'usuario': usuario, 'cor_preferida': cor_preferida})
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
    response.delete_cookie('cor_preferida')
    return response


def personalizar(request):
    if request.method == 'POST':
        cor_preferida = request.POST.get('cor_preferida')
        request.session['cor_preferida'] = cor_preferida
        response = redirect('dashboard')
        response.set_cookie('cor_preferida', cor_preferida, max_age=3600)
        return response
    return render(request, 'biblioteca/personalizar.html')
