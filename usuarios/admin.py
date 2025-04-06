import openpyxl
from django.contrib import admin
from django.apps import apps
from django.db import models
from django.http import HttpResponse

# Função para exportar dados como Excel
def export_as_excel(modeladmin, request, queryset):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Exportação de Dados"

    # Cabeçalhos
    columns = [field for field in modeladmin.list_display]
    ws.append(columns)

    # Adiciona as linhas de dados
    for obj in queryset:
        row = []
        for field in modeladmin.list_display:
            value = getattr(obj, field) if hasattr(obj, field) else None
            row.append(str(value) if value is not None else '')
        ws.append(row)

    # Cria a resposta HTTP com o arquivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="export.xlsx"'
    wb.save(response)
    return response

# Função para descriptografar a senha, se disponível no modelo
def senha_descriptografada(obj):
    try:
        return obj.descriptografar_senha()  # Adapte conforme o seu modelo
    except Exception:
        return "Erro na descriptografia"
senha_descriptografada.short_description = "Senha Descriptografada"

# Obtém todas as tabelas do modelo
models = apps.get_models()

# Registra cada modelo no Django Admin
for model in models:
    try:
        class ModelAdmin(admin.ModelAdmin):
            # Inicializa a lista de campos que serão exibidos no list_display
            list_display = []
            list_filter = []

            # Obtém os campos do modelo e adiciona a senha descriptografada
            for field in model._meta.fields:
                # Verifica se o campo não é o id e não é um TextField
                if field.name != 'id' and field.get_internal_type() != 'TextField':
                    list_display.append(field.name)
                    list_filter.append(field.name)

            # Adiciona a senha descriptografada ao list_display
            if hasattr(model, 'descriptografar_senha'):
                list_display.append('senha_descriptografada')

            # Adiciona a ação de exportar para o Excel
            actions = [export_as_excel]

            # Função para a senha descriptografada
            def senha_descriptografada(self, obj):
                try:
                    return obj.descriptografar_senha()
                except Exception:
                    return "Erro na descriptografia"

            # Adiciona os métodos de visualização
            readonly_fields = ['senha_descriptografada']  # Definir como readonly

        # Registra o modelo no Django Admin
        admin.site.register(model, ModelAdmin)
    except admin.sites.AlreadyRegistered:
        pass