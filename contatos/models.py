from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField(default=0)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    is_adim = models.BooleanField(
        default=False)  #booleano FALSE pra dizer que por padrao TODOS usuarios NAo sao,por default, administrador
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAMED_FIELD = 'email'
    REQUIRED_FIELD = ['nome', 'idade', 'senha']

    class Meta:
        verbose_name_plural = 'usuarios'
        db_table = 'usuario'
        verbose_name = 'usuario'
        ordering = ['-created_at']  # created_at do mais recente

    def __str__(self):
        return self.nome

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return False

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Contato(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='contatos')
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contato'
        verbose_name = 'contato'
        ordering = ['nome']  # ordem alfabetica
        unique_together = ('usuario', 'email')

    def __str__(self):
        return self.nome
