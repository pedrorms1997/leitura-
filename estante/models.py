# estante/models.py
from django.db import models
from django.conf import settings

class Livro(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='livros')
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, blank=True)
    editora = models.CharField(max_length=255, blank=True)
    ano_publicacao = models.IntegerField(null=True, blank=True)
    idioma = models.CharField(max_length=50, blank=True)
    isbn = models.CharField(max_length=50, blank=True)
    paginas = models.IntegerField(null=True, blank=True)
    sinopse = models.TextField(blank=True)
    capa_url = models.URLField(blank=True)
    pagina_atual = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return f"{self.titulo} ({self.usuario.username})"
