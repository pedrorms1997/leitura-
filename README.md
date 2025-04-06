
# Leitura+

Leitura+ é um aplicativo web desenvolvido com Django, que permite o acompanhamento de sessões de leitura, focado em leitores que desejam registrar seu progresso e estatísticas.

Criamos esse projeto para aplicar funcionalidades aprendidas na disciplina Interface Homem-Máquina (IHM).

## 📚 Funcionalidades

- Cadastro e visualização de sessões de leitura
- Registro de tempo de leitura
- Controle de páginas lidas
- Interface para acompanhamento de progresso

## 🛠 Tecnologias Utilizadas

- Python 3
- Django
- SQLite (banco de dados padrão)
- HTML/CSS (via templates Django)
- Google Books API
- Gemini AI (API da Google para geração de texto)

## 🔌 Integrações com APIs Externas

### 📖 Google Books API
Utilizamos a [API do Google Livros](https://developers.google.com/books) para buscar informações sobre livros, como:
- Título
- Autor
- Capa
- Descrição

Essa API é pública e pode ser utilizada **sem autenticação** para a maioria das requisições básicas, como buscas de livros por título ou autor.

### 🤖 Gemini API (Google Generative AI)
A [API do Gemini](https://ai.google.dev) é usada para gerar recomendações inteligentes de leitura com base no histórico do usuário ou preferências informadas. Essa integração permite que o sistema ofereça sugestões personalizadas e conversacionais sobre livros.

Para utilizar a API do Gemini, é necessário configurar sua chave no arquivo `.env`:

```env
GEMINI_API_KEY=sua-chave-do-gemini
```

## 🚀 Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/leitura-mais.git
cd leitura-mais
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo básico:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
GEMINI_API_KEY=sua-chave-do-gemini
```

Você pode gerar uma nova chave secreta executando no terminal:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse em `http://127.0.0.1:8000/`.

## 🗂 Estrutura do Projeto

- `manage.py`: script principal para gerenciamento do Django
- `sessoes/`: app responsável pelas sessões de leitura
  - `models.py`: definição dos modelos (banco de dados)
  - `views.py`: lógica das páginas
  - `admin.py`: integração com o admin do Django
  - `urls.py`: rotas do app
  - `migrations/`: arquivos de migração de banco

---

## 👨‍💻 Desenvolvedores
- **Pedro Moraes**  
  [GitHub](https://github.com/pedrorms1997) • [LinkedIn](https://www.linkedin.com/in/pedro-rodrigues-m-b69704101/)
