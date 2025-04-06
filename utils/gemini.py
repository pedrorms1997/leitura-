import sys
sys.path.insert(0,'')
from Django_conf.settings import GEMINI_KEY
from time import sleep
from google.api_core.exceptions import ResourceExhausted
import google.generativeai as genai
import json
import requests

def buscar_capa_google_livros(titulo, autor):
    import requests
    query = f"{titulo} {autor}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

    try:
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "items" in data and data["items"]:
                volume_info = data["items"][0].get("volumeInfo", {})
                image_links = volume_info.get("imageLinks", {})
                return image_links.get("thumbnail") or image_links.get("smallThumbnail")
    except Exception as e:
        print(f"Erro na busca da capa: {e}")
    return None

def realizar_consulta_gemini(
    prompt:str, 
    api_key:str=None
):
    """_summary_

    Args:
        prompt (str): _description_
        api_key (str, optional): _description_. Defaults to None.

    Returns:
        Exemplo de retorno: {
            'ano_publicacao': 1949,
            'autor': 'George Orwell',
            'editora': 'Companhia das Letras',
            'genero': ['Ficção Distópica', 'Romance'],
            'idioma': 'Português',
            'isbn': '978-8535913614',
            'paginas': 416,
            'sinopse': 'Em um futuro distópico, Winston Smith vive sob a vigilância '
                'constante do Partido e luta contra a opressão em uma sociedade '
                'totalitária.',
            'titulo': '1984'
        }
    """
    try:
        
        if not api_key:
            api_key = GEMINI_KEY
        
        # Cabeçalhos da requisição
        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "contents" :{
                'parts' : [
                    {
                        'text' : f'prompt: {prompt}'
                    }
                ]
            },
                "generationConfig": {
                "temperature": 1.0,   # Deixe o mais alto possível (0.9~1.0)
                "topP": 1.0,          # Valor alto para mais diversidade
                "topK": 50,           # Quanto mais alto, mais variação (até 100 ou mais, se aceito pela API)
                "response_mime_type": "application/json"
            }
        }
        
        data = json.dumps(data)

        # Envia a requisição POST para a API Gemini 1.5
        response = requests.post(
            rf"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}", 
            headers=headers, 
            data=data, 
            verify=False
        )
        retorno = json.loads(response.content)
        
        tokens = retorno['usageMetadata']
        tokens_input = tokens['promptTokenCount']
        tokens_output = tokens['candidatesTokenCount']
        tokens_total = tokens['totalTokenCount']
        
        candidates = retorno['candidates']
        cand_content = candidates[0]['content']
        cont_parts = cand_content['parts']
        retorno_text= cont_parts[0]['text']
        retorno_text = str(retorno_text).replace('```json','').replace('```','').replace('\\n','')
        retorno_text = json.loads(retorno_text)

        return retorno_text
    
    except:
        return None

def consultar_um_livro(
    nome_livro:str, 
    api_key:str=None
):
    """_summary_

    Args:
        prompt (str): _description_
        api_key (str, optional): _description_. Defaults to None.

    Returns:
        Exemplo de retorno: {
            'ano_publicacao': 1949,
            'autor': 'George Orwell',
            'editora': 'Companhia das Letras',
            'genero': ['Ficção Distópica', 'Romance'],
            'idioma': 'Português',
            'isbn': '978-8535913614',
            'paginas': 416,
            'sinopse': 'Em um futuro distópico, Winston Smith vive sob a vigilância '
                'constante do Partido e luta contra a opressão em uma sociedade '
                'totalitária.',
            'titulo': '1984'
        }
    """
    try:
        
        if not api_key:
            api_key = GEMINI_KEY
        
        # Cabeçalhos da requisição
        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "contents" :{
                'parts' : [
                    {
                        'text' : f'''
                            prompt: Me traga informações do livro:
                            Segue um exemplo do JSon formatado.
                            {
                                "titulo": "O Senhor dos Anéis: A Sociedade do Anel",
                                "autor": "J.R.R. Tolkien",
                                "editora": "HarperCollins",
                                "ano_publicacao": 1954,
                                "idioma": "Português",
                                "genero": ["Fantasia", "Aventura"],
                                "isbn": "978-8595080500",
                                "paginas": 576,
                                "sinopse": "Na primeira parte da épica trilogia, Frodo Bolseiro parte em uma jornada para destruir o Um Anel, forjado pelo Senhor do Escuro Sauron.",
                            }
                        '''
                    }
                ]
            },
                "generationConfig": {
                "temperature": 1.0,   # Deixe o mais alto possível (0.9~1.0)
                "topP": 1.0,          # Valor alto para mais diversidade
                "topK": 50,           # Quanto mais alto, mais variação (até 100 ou mais, se aceito pela API)
                "response_mime_type": "application/json"
            }
        }
        
        data = json.dumps(data)

        # Envia a requisição POST para a API Gemini 1.5
        response = requests.post(
            rf"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}", 
            headers=headers, 
            data=data, 
            verify=False
        )
        retorno = json.loads(response.content)
        
        tokens = retorno['usageMetadata']
        tokens_input = tokens['promptTokenCount']
        tokens_output = tokens['candidatesTokenCount']
        tokens_total = tokens['totalTokenCount']
        
        candidates = retorno['candidates']
        cand_content = candidates[0]['content']
        cont_parts = cand_content['parts']
        retorno_text= cont_parts[0]['text']
        retorno_text = str(retorno_text).replace('```json','').replace('```','').replace('\\n','')
        retorno_text = json.loads(retorno_text)

        return retorno_text
    
    except:
        return None   

if __name__ == "__main__":
    retorno = realizar_consulta_gemini(
        prompt= """
            Me recomende um unico livro. E me retorne em um Json formatado com a recomendação.
            Segue um exemplo do JSon formatado.
            {
                "titulo": "O Senhor dos Anéis: A Sociedade do Anel",
                "autor": "J.R.R. Tolkien",
                "editora": "HarperCollins",
                "ano_publicacao": 1954,
                "idioma": "Português",
                "genero": ["Fantasia", "Aventura"],
                "isbn": "978-8595080500",
                "paginas": 576,
                "sinopse": "Na primeira parte da épica trilogia, Frodo Bolseiro parte em uma jornada para destruir o Um Anel, forjado pelo Senhor do Escuro Sauron.",
            }
        """,
    )
    
    ...