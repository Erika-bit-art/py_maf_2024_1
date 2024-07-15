import hashlib

from django import forms
from django.contrib.auth.hashers import check_password

from biblioteca.models import Usuario, Livro


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class UsuarioForm(BootstrapModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'idade', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class LivroForm(BootstrapModelForm):
    class Meta:
        model = Livro
        fields = ['nome', 'ano_de_publicacao', 'pais', 'autor', 'sinopse']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'exemplo@dominio.com'
    }))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Sua senha'
    }))





def clean(self):
    email = self.cleaned_data.get('email')
    password = self.cleaned_data.get('password')

    if email and password:
        try:
            usuario = Usuario.objects.get(email=email)
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if usuario.password != hashed_password:
                raise forms.ValidationError('Senha incorreta.')
        except Usuario.DoesNotExist:
            raise forms.ValidationError('Email não encontrado.')

    return self.cleaned_data


