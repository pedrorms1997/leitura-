# estante/views.py
import requests
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render,redirect, get_object_or_404
from .models import Livro

@login_required
def estante_view(request):
    livros = Livro.objects.filter(usuario=request.user).order_by('-id')
    return render(request, 'estante/estante.html', {'livros': livros})

@require_GET
@login_required
def buscar_livros(request):
    q = request.GET.get('q', '')
    if len(q) < 2:
        return JsonResponse({'items': []})
    
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={q}&langRestrict=pt')
    return JsonResponse(response.json())

@require_POST
@login_required
def salvar_livro(request):
    try:
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)

        print('📥 Dados recebidos para salvar livro:', data)
        
        livro,created = Livro.objects.get_or_create(
            usuario=request.user,
            titulo=data.get('titulo') or '',
            autor=data.get('autor') or '',
            editora=data.get('editora') or '',
            ano_publicacao=int(data.get('ano_publicacao')) if data.get('ano_publicacao') else None,
            idioma=data.get('idioma') or '',
            isbn=data.get('isbn') or '',
            paginas=int(data.get('paginas')) if data.get('paginas') else None,
            sinopse=data.get('sinopse') or '',
            capa_url=data.get('capa_url') or ''
        )
        
        return JsonResponse({'success': True, 'livro_id': livro.id})

    except json.JSONDecodeError as e:
        print('❌ JSON malformado:', e)
        return HttpResponseBadRequest('Requisição malformada.')

    except Exception as e:
        print('❌ Erro ao salvar livro:', e)
        return HttpResponseBadRequest(f'Erro ao salvar livro: {e}')


@require_POST
@login_required
def excluir_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id, usuario=request.user)
    livro.delete()
    return redirect('estante:estante')

@login_required
def faixa_estante(request):
    livros = Livro.objects.filter(usuario=request.user)
    return render(request, 'estante/faixa_estante.html', {'livros': livros})