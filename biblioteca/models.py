from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
import base64


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, idade, password=None, is_admin=False, is_active=False):
        if not email:
            raise ValueError('O campo email é obrigatório!')

        if not nome:
            raise ValueError('O campo nome é obrigatório!')

        user = self.model(
            email=self.normalize_email(email),
            nome=nome,
            idade=idade,
        )
        user.set_password(password)
        user.is_admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, idade, password=None):
        user = self.create_user(
            email,
            nome=nome,
            idade=idade,
            password=password,
            is_admin=True,
            is_active=True
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'idade', 'password']


    class Meta:
        verbose_name_plural = 'usuarios'
        db_table = 'usuario'
        verbose_name = 'usuario'
        ordering = ['-created_at']  # created_at do mais recente

    def __str__(self):
        return self.nome

    def get_by_natural_key(self, email):
        return self.get(email=email)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True


class Livro(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='livros')
    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=100, default='')
    sinopse = models.CharField(max_length=500, default='')
    ano_de_publicacao = models.CharField(max_length=4)
    pais = models.CharField(max_length=15, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categoria = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'livro'
        verbose_name = 'livro'
        ordering = ['nome']  # ordem alfabetica

    def __str__(self):
        return self.nome
