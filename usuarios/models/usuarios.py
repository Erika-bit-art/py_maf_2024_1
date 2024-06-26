from django.db import models

class Usuario(models.Model):   # herança(classe e subclasse)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)

    class Meta:
        db_table = 'usuario'  # define o nome da tabela

    def __str__(self):
        return self.nome

