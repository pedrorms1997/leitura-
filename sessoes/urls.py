from django.urls import path
from . import views

app_name = 'sessoes'

urlpatterns = [
    path('', views.sessoes_view, name='sessoes'),
    path('iniciar/', views.iniciar_sessao, name='iniciar'),
    path('parar/', views.parar_sessao, name='parar'),
    path('atualizar-pagina/', views.atualizar_pagina_atual, name='atualizar_pagina'),
]
