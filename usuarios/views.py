import hashlib

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models.usuarios import Usuario

def registro(request):
    if request.method == 'POST':
        # resgatando as informacoes vindas do formulario
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # criptografando senha
        data = senha.encode('utf-8')
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data)
        senha_criptografada = sha256_hash.hexdigest()
        Usuario.objects.create(nome=nome, idade=idade, email=email, senha=senha_criptografada)

    return render(request, 'usuarios/registro.html')


def login(request):
    if request.method == 'POST ':

        email = request.POST.get('email')
        senha = request.POST.get('senha')

        #criptografando senha
        sha256_hash = hashlib.sha256()
        sha256_hash.update(senha.encode('utf-8'))
        senha_criptograda = sha256_hash.hexdigest()

        try:
            usuarios = Usuario.objects.get(email=email, senha=senha)
            request.session['usuario_id'] = usuarios.id
            return redirect('personalizar')

        except Usuario.DoesNotExist:
            return HttpResponse('Nome de usuário ou senha inválidos.')

    return render(request, 'usuarios/login.html')

def personalizar(request):
    if request.method == 'POST':
        cor_preferida = request.POST.get('cor_preferida')
        request.session['cor_preferida'] = cor_preferida
        response = redirect('dashboard')
        response.set_cookie('cor_preferida', cor_preferida, max_age=3600)
        return response
    return render(request, 'usuarios/personalizar.html')

def dashbord(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)
    cor_preferida = request.COOKIES.get('cor_preferida','default')
    return render(request, 'usuarios/dashboard.html', {'usuario': usuario, 'cor_preferida':cor_preferida})

def logout(request):
    request.session.flush()
    response = redirect('login')
    response.delete_cookie('cor_preferida')
    return response





