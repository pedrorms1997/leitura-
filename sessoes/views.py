from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import SessaoLeitura
from estante.models import Livro

@login_required
def sessoes_view(request):
    livros = Livro.objects.filter(usuario=request.user)
    return render(request, 'sessoes/sessoes.html', {'livros': livros})

@login_required
def iniciar_sessao(request):
    if request.method == 'POST':
        livro_id = request.POST.get('livro_id')
        pagina_atual = request.POST.get('pagina_inicial')

        livro = get_object_or_404(Livro, id=livro_id, usuario=request.user)

        sessao = SessaoLeitura.objects.create(
            usuario=request.user,
            livro=livro,
            inicio=timezone.now(),
            pagina_inicial=pagina_atual
        )
        return JsonResponse({'status': 'ok', 'sessao_id': sessao.id})
    return JsonResponse({'status': 'erro'}, status=400)

@login_required
def parar_sessao(request):
    if request.method == 'POST':
        sessao_id = request.POST.get('sessao_id')
        pagina_final = request.POST.get('pagina_final')

        try:
            sessao = SessaoLeitura.objects.get(id=sessao_id, usuario=request.user)
            sessao.fim = timezone.now()
            sessao.pagina_final = pagina_final
            sessao.save()

            # Atualiza a página atual do livro
            livro = sessao.livro
            livro.pagina_atual = pagina_final
            livro.save()

            return JsonResponse({'status': 'ok'})
        except SessaoLeitura.DoesNotExist:
            return JsonResponse({'status': 'erro'}, status=404)

    return JsonResponse({'status': 'erro'}, status=400)

@login_required
def atualizar_pagina_atual(request):
    if request.method == 'POST':
        livro_id = request.POST.get('livro_id')
        nova_pagina = request.POST.get('pagina_atual')

        livro = get_object_or_404(Livro, id=livro_id, usuario=request.user)
        livro.pagina_atual = nova_pagina
        livro.save()
        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'status': 'erro'}, status=400)
