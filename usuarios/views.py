from django.contrib.auth.views import LoginView
from .forms import LoginForm, RegistroForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Usuario
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class RegistroView(CreateView):
    model = Usuario
    form_class = RegistroForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('usuarios:login')

class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm

@method_decorator(login_required, name='dispatch')
class PerfilView(View):
    def get(self, request):
        return render(request, 'usuarios/perfil.html')

    def post(self, request):
        user = request.user
        foto = request.FILES.get('foto_perfil')
        nome = request.POST.get('nome')
        bio = request.POST.get('bio')

        if foto:
            user.foto_perfil = foto
        if nome:
            user.username = nome  # Agora alterando o nome exibido
        if bio:
            user.bio = bio
        user.save()

        return redirect('usuarios:perfil')
