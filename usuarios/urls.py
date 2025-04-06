# usuarios/urls.py
from django.urls import path
from .views import UsuarioLoginView, RegistroView, PerfilView
from django.contrib.auth.views import LogoutView

app_name = 'usuarios'  # Isso ativa o namespace

urlpatterns = [
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='usuarios:login'), name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
]
