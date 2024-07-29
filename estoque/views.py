import base64
import hashlib
from django.contrib.auth.decorators import login_required, user_passes_test

import io
from tkinter import Image

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from estoque.forms import ProdutoForm, UsuarioForm, LoginForm, Usuario, Produto

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
            return render(request, 'estoque/registro.html', {'form': form})
    else:
        form = UsuarioForm()
        return render(request, 'estoque/registro.html', {'form': form})


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
    return render(request, 'estoque/login.html', {'form': form})


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
            produtos = Produto.objects.filter(usuario=usuario)

            context = {
                'usuario': usuario,
                'produtos': produtos,
            }
        return render(request, 'estoque/dashboard.html', context)
    else:
        return redirect('login')


def adicionar_produto(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        if request.method == 'POST':
            form = ProdutoForm(request.POST)
            if form.is_valid():
                produto = form.save(commit=False)
                produto.usuario_id = request.session.get('usuario_id')
                produto.save()
                messages.success(request, f'Produto \'{produto.nome}\' adicionado com sucesso!')
                return redirect('dashboard')
            else:
                return render(request, 'estoque/adicionar_produto.html', {'form': form})
        else:
            form = ProdutoForm()
        return render(request, 'estoque/adicionar_produto.html', {'form': form})
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
            pass  # Se a idade não for um número, ignorar este filtro.

    usuarios = usuarios.filter(is_admin=False).annotate(produtos_count=Count('produtos'))
    return render(request, 'estoque/listar_usuarios.html', {'usuarios': usuarios})


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


@login_required
def editar_produto(request, produto_id):
    # Obtém o produto ou retorna 404 se não encontrado
    produto = get_object_or_404(Produto, id=produto_id, usuario_id=request.session.get('usuario_id'))

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            produto = form.save()  # Salva o produto sem manipulação de imagem
            messages.success(request, f'Produto \'{produto.nome}\' atualizado com sucesso!')
            return redirect('dashboard')  # Redireciona para o dashboard ou outra página desejada
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'estoque/editar_produto.html', {'form': form, 'produto': produto})


@login_required
def excluir_produto(request, produto_id):
    # Obtém o produto ou retorna 404 se não encontrado
    produto = get_object_or_404(Produto, id=produto_id, usuario_id=request.session.get('usuario_id'))

    if request.method == 'POST':
        produto.delete()  # Exclui o produto
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('dashboard')  # Redireciona para o dashboard ou outra página desejada

    return render(request, 'estoque/excluir_produto.html', {'produto': produto})
