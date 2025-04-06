import json
import random
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from estante.models import Livro
from utils.gemini import realizar_consulta_gemini

EXEMPLOS_JSON = [
    {
        "titulo": "O Senhor dos Anéis: A Sociedade do Anel",
        "autor": "J.R.R. Tolkien",
        "editora": "HarperCollins",
        "ano_publicacao": 1954,
        "idioma": "Português",
        "genero": ["Fantasia", "Aventura"],
        "isbn": "978-8595080500",
        "paginas": 576,
        "sinopse": "Na primeira parte da épica trilogia, Frodo Bolseiro parte em uma jornada para destruir o Um Anel, forjado pelo Senhor do Escuro Sauron."
    },
    {
        "titulo": "Duna",
        "autor": "Frank Herbert",
        "editora": "Aleph",
        "ano_publicacao": 1965,
        "idioma": "Português",
        "genero": ["Ficção Científica", "Aventura"],
        "isbn": "978-8576572001",
        "paginas": 680,
        "sinopse": "Em um futuro distante, Paul Atreides lidera uma rebelião em um planeta deserto para controlar o recurso mais valioso do universo."
    },
    {
        "titulo": "Cem Anos de Solidão",
        "autor": "Gabriel García Márquez",
        "editora": "Record",
        "ano_publicacao": 1967,
        "idioma": "Português",
        "genero": ["Realismo Mágico", "Romance"],
        "isbn": "978-8501064254",
        "paginas": 448,
        "sinopse": "A saga da família Buendía ao longo de gerações na mítica cidade de Macondo, onde o real e o fantástico se misturam."
    }
]

GENEROS = [
    "Ficção Científica", "Ficção Histórica", "Romance", "Drama", "Mistério",
    "Terror", "Fantasia", "Aventura", "Poesia", "Biografia", "Filosofia",
    "Psicologia", "Sociologia", "Tecnologia", "Thriller", "Clássico", "Distopia"
]

EPOCAS = [
    "século XII", "século XV", "século XVIII", "anos 1920", "anos 1950",
    "anos 1970", "futuro distante", "Idade Média", "Revolução Industrial",
    "época vitoriana", "era espacial", "renascimento", "era cyberpunk"
]

@login_required
def recomendacao_personalizada(request):
    sugestao = None

    if request.method == "POST":
        modo = request.POST.get("modo", "manual")
        texto_usuario = request.POST.get("texto")

        # Gênero e época aleatórios
        genero_escolhido = random.choice(GENEROS)
        epoca_escolhida = random.choice(EPOCAS)
        contexto_extra = f"Gere um livro ambientado na época de {epoca_escolhida} e que pertença ao gênero '{genero_escolhido}'."

        # Exemplo de JSON aleatório
        exemplo_json = json.dumps(random.choice(EXEMPLOS_JSON), ensure_ascii=False, indent=4)

        if modo == "historico":
            livros = Livro.objects.filter(usuario=request.user)
            if not livros.exists():
                return render(request, 'recomendacoes/personalizada.html', {'erro': 'Você ainda não possui livros cadastrados.'})

            titulos = [livro.titulo for livro in livros]
            random.shuffle(titulos)
            lista = "\n".join(f"- {titulo}" for titulo in titulos)

            prompt = f'''
{contexto_extra}

Considere que quero explorar novos estilos. Recomende um livro que talvez não seja óbvio, ou que fuja um pouco do padrão baseado nos títulos abaixo.
Responda apenas com um JSON com as informações do livro.
Formato de exemplo:
{exemplo_json}
Livros cadastrados:
{lista}
'''
        else:
            prompt = f'''
{contexto_extra}

Com base no seguinte desejo de leitura do usuário: "{texto_usuario}", recomende um único livro.
Seja criativo e traga algo diferente do esperado.
Formato de resposta:
{exemplo_json}
'''

        resultado = realizar_consulta_gemini(prompt)

        if resultado:
            query = f"intitle:{resultado['titulo']}"
            if resultado.get('autor'):
                query += f"+inauthor:{resultado['autor']}"

            response = requests.get(
                'https://www.googleapis.com/books/v1/volumes',
                params={
                    'q': query,
                    'maxResults': 5,
                    'printType': 'books',
                    'langRestrict': 'pt'
                },
                timeout=10
            )

            if response.status_code == 200:
                items = response.json().get('items', [])
                for item in items:
                    image_links = item.get('volumeInfo', {}).get('imageLinks', {})
                    if 'thumbnail' in image_links:
                        resultado['capa_url'] = image_links['thumbnail'].replace('http://', 'https://')
                        break
                else:
                    resultado['capa_url'] = '/static/site/sem_capa.png'

            sugestao = resultado

    return render(request, 'recomendacoes/personalizada.html', {'sugestao': sugestao})


@require_POST
@login_required
def salvar_livro_recomendado(request):
    try:
        data = request.POST

        livro, _ = Livro.objects.get_or_create(
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

        return redirect('estante:estante')

    except Exception as e:
        print('Erro ao salvar livro recomendado:', e)
        return redirect('recomendacoes:personalizada')
