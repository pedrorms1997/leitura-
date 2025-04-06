from django.urls import path
from . import views

app_name = 'recomendacoes'

urlpatterns = [
    path('personalizada/', views.recomendacao_personalizada, name='personalizada'),
    path('salvar/', views.salvar_livro_recomendado, name='salvar_livro'),
]
