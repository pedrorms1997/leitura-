from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sessoes.models import SessaoLeitura
from estante.models import Livro

def formatar_tempo_legivel(segundos):
    total_segundos = int(segundos)
    dias, resto = divmod(total_segundos, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, segundos = divmod(resto, 60)

    partes = []
    if dias:
        partes.append(f"{dias} dia{'s' if dias > 1 else ''}")
    if horas:
        partes.append(f"{horas} hora{'s' if horas > 1 else ''}")
    if minutos:
        partes.append(f"{minutos} minuto{'s' if minutos > 1 else ''}")
    if segundos or not partes:
        partes.append(f"{segundos} segundo{'s' if segundos != 1 else ''}")

    return ', '.join(partes[:-1]) + f" e {partes[-1]}" if len(partes) > 1 else partes[0]

@login_required
def painel_estatisticas(request):
    livros = Livro.objects.filter(usuario=request.user)
    sessoes = SessaoLeitura.objects.filter(livro__usuario=request.user)

    total_paginas_lidas = sum(
        [s.pagina_final - s.pagina_inicial for s in sessoes if s.pagina_final and s.pagina_inicial]
    )
    total_tempo = sum(
        [(s.fim - s.inicio).total_seconds() for s in sessoes if s.inicio and s.fim], 0.0
    )
    tempo_medio = (total_tempo / len(sessoes)) if sessoes else 0

    livros_info = []
    for livro in livros:
        sessoes_livro = sessoes.filter(livro=livro)
        paginas_lidas = sum(
            [s.pagina_final - s.pagina_inicial for s in sessoes_livro if s.pagina_final and s.pagina_inicial]
        )
        tempo_livro = sum(
            [(s.fim - s.inicio).total_seconds() for s in sessoes_livro if s.inicio and s.fim], 0.0
        )
        percentual = round((paginas_lidas / livro.paginas) * 100, 1) if livro.paginas else 0

        livros_info.append({
            'titulo': livro.titulo,
            'autor': livro.autor,
            'capa_url': livro.capa_url,
            'paginas_lidas': paginas_lidas,
            'total_paginas': livro.paginas,
            'percentual': percentual,
            'tempo_total': formatar_tempo_legivel(tempo_livro),
        })

    contexto = {
        'total_paginas_lidas': total_paginas_lidas,
        'tempo_total': formatar_tempo_legivel(total_tempo),
        'tempo_medio': formatar_tempo_legivel(tempo_medio),
        'livros_concluidos': sum(1 for l in livros_info if l['percentual'] >= 100),
        'total_livros': livros.count(),
        'livros_info': livros_info,
    }

    return render(request, 'estatisticas/estatisticas.html', contexto)
