from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

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
    REQUIRED_FIELDS = ['nome', 'idade']

    class Meta:
        verbose_name_plural = 'usuarios'
        db_table = 'usuario'
        verbose_name = 'usuario'
        ordering = ['-created_at']

    def __str__(self):
        return self.nome

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

class Registro(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='registros')
    atleta = models.CharField(max_length=100)
    modalidade = models.CharField(max_length=100, default='')
    pais = models.CharField(max_length=500, default='')
    medalha = models.CharField(max_length=50, default='')
    ano = models.CharField(max_length=100)
    local_sede = models.CharField(max_length=15, default='')
    momento = models.CharField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'registro'
        verbose_name = 'registro'
        ordering = ['atleta']

    def __str__(self):
        return self.atleta

