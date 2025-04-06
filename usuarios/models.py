# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.templatetags.static import static
import os
from datetime import datetime
from django.utils.text import slugify

def caminho_foto_perfil(instance, filename):
    nome_base, extensao = os.path.splitext(filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    nome_arquivo = f"{slugify(instance.username)}_{instance.pk}_{timestamp}{extensao}"
    return f'perfil/{nome_arquivo}'

class Usuario(AbstractUser):
    xp = models.IntegerField(default=0, help_text="Experiência acumulada pelo usuário.")
    nivel = models.IntegerField(default=1, help_text="Nível atual do usuário com base no XP.")
    
    foto_perfil = models.ImageField(upload_to=caminho_foto_perfil, null=True, blank=True,default='perfil/default_avatar.png')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

    def adicionar_xp(self, quantidade):
        self.xp += quantidade
        while self.xp >= self.nivel * 100:
            self.nivel += 1
        self.save()

    @property
    def foto_perfil_url(self):
        if self.foto_perfil:
            return self.foto_perfil.url
        return os.path.join(settings.MEDIA_URL, 'perfil/avatar_padrao.png')

