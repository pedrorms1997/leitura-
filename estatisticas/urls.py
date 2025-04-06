from django.urls import path
from .views import painel_estatisticas

app_name = 'estatisticas'

urlpatterns = [
    path('', painel_estatisticas, name='painel'),
]
