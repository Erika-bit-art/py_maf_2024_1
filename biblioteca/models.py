from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=255, default='', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'idade', 'password']

    class Meta:
        verbose_name_plural = 'usuarios'
        db_table = 'usuario'
        verbose_name = 'usuario'
        ordering = ['-created_at']

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

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
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

    class Meta:
        db_table = 'livro'
        verbose_name = 'livro'
        ordering = ['nome']  # ordem alfabetica


    def __str__(self):
        return self.nome

