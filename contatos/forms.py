import hashlib

from django import forms
from django.contrib.auth.hashers import check_password

from contatos.models import Usuario, Contato


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class UsuarioForm(BootstrapModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'idade', 'email', 'senha']
        widgets = {
            'senha': forms.PasswordInput(),
        }


class ContatoForm(BootstrapModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'telefone', 'logradouro', 'bairro', 'cidade', 'uf', 'cep']
        widgets = {
            'telefone': forms.TextInput(attrs={'data-mask': '(00) 00000-0000'}),
            'cep': forms.TextInput(attrs={'data-mask': '00000-0000'}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'exemplo@dominio.com'
    }))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Sua senha'

     }))

def clean(self):  # NAO SEI SE TEM QUE DEIXAR OU APAGAR PQ TEM DEOIS 'DEF CLEAN' ESSE (O VELHO) E O DE CIMA (MAIS RECENTE)
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        senha = cleaned_data.get('senha')

        if email and senha:
            try:
                usuario = Usuario.objects.get(email=email)
                # Verifique a senha criptografada
                hashed_password = hashlib.sha256(senha.encode('utf-8')).hexdigest()
                if usuario.senha != hashed_password:
                    raise forms.ValidationError('Senha incorreta.')
            except Usuario.DoesNotExist:
                raise forms.ValidationError('Email não encontrado.')

        return cleaned_data


class PasswordChangeForm(forms.Form):        # TA ASSOCIADO AO VIEWS DE 'DEF MUDAR SENHA' QUE NAO FOI FINALIZADO AINDA...
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Sua senha atual'
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Nova senha'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirme a nova senha'

    }))


    def clean(self):                        # TA ASSOCIADO AO VIEWS DE 'DEF MUDAR SENHA' QUE NAO FOI FINALIZADO AINDA...
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('Confirmação de senha inválida')

        if new_password and old_password and new_password == old_password:
            raise forms.ValidationError('A senha nova não pode ser igual a senha antiga')

        return cleaned_data





