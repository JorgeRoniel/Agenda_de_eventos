from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Eventos(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    dataEvento = models.DateField()
    dataCriacao = models.DateField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def get_dataEvento(self):
        return self.dataEvento.strftime('%d/%m/%Y')

    def get_dataEvento_input_evento(self):
        return self.dataEvento.strftime('%Y-%m-%d')