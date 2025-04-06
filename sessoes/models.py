from django.db import models
from django.conf import settings
from estante.models import Livro

class SessaoLeitura(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    inicio = models.DateTimeField()
    fim = models.DateTimeField(null=True, blank=True)
    pagina_inicial = models.IntegerField()
    pagina_final = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.usuario.username} - {self.livro.titulo} ({self.inicio.strftime('%d/%m/%Y %H:%M')})"
