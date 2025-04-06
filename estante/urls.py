# estante/urls.py
from django.urls import path
from .views import buscar_livros, estante_view, salvar_livro,excluir_livro,faixa_estante

app_name = 'estante'

urlpatterns = [
    path('', estante_view, name='estante'),
    path('busca/', buscar_livros, name='busca'),
    path('salvar/', salvar_livro, name='salvar'),
    path('excluir/<int:livro_id>/', excluir_livro, name='excluir'),
    path('faixa/', faixa_estante, name='faixa_estante'),

]
