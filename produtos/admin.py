from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Produto, Categoria, Marca, Cliente, Pedido,
    ItemPedido, FormaPagamento, EnderecoEntrega,
    Estoque, UsuarioAdmin
)
from .models import (
    Produto,
    ItemPedido,
)

# 🌟 Customização do site admin
class MyAdminSite(admin.AdminSite):
    site_header = "Loja de Make 💋"
    site_title = "Painel da Loja de Make"
    index_title = "Bem-vinda, Jessica!"

admin_site = MyAdminSite(name='meuadmin')

# 💄 Admin do Produto com imagem, filtro e busca
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_formatado', 'categoria_nome', 'imagem_preview')
    readonly_fields = ('imagem_preview',)
    search_fields = ('nome', 'categoria__nome')
    list_filter = ('categoria', 'marca')

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="70" style="border-radius: 4px; object-fit: cover;" />', obj.imagem.url)
        return "-"
    imagem_preview.short_description = "Imagem"

    def preco_formatado(self, obj):
        return f"R$ {obj.preco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    preco_formatado.short_description = 'Preço'

    def categoria_nome(self, obj):
        return obj.categoria.nome
    categoria_nome.short_description = 'Categoria'

# 🧾 Outros admins (você pode personalizar depois se quiser!)
class UsuarioAdminInline(admin.ModelAdmin):
    list_display = ('nome_completo', 'cargo')

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'email', 'telefone', 'data_cadastro')
    search_fields = ('nome', 'cpf', 'email')

# Classe Inline para exibir Itens do Pedido diretamente no PedidoAdmin
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0 # Não exibe linhas extras vazias por padrão
    raw_id_fields = ['produto'] # Útil para buscar produtos se você tiver muitos

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Correção aqui: use 'forma_pagamento_selecionada'
    list_display = (
        'pk', # ID do pedido
        'usuario',
        'forma_pagamento_selecionada', # <-- CORREÇÃO: ERA 'forma_pagamento'
        'total',
        'status',
        'data_pedido',
    )
    list_filter = ('status', 'data_pedido', 'forma_pagamento_selecionada')
    search_fields = ('usuario__username', 'pk') # Permite buscar por nome de usuário e ID do pedido
    inlines = [ItemPedidoInline] # Adiciona o inline para ver os itens do pedido
    raw_id_fields = ('usuario', 'endereco_entrega', 'forma_pagamento_selecionada') # Útil para selects grandes

    # Se você quiser permitir a edição de status diretamente na lista
    list_editable = ('status',)

    # Campos que serão exibidos na página de detalhes do pedido
    fieldsets = (
        (None, {
            'fields': ('usuario', 'endereco_entrega', 'forma_pagamento_selecionada', 'total', 'status'),
        }),
        ('Datas', {
            'fields': ('data_pedido',),
            'classes': ('collapse',), # Opcional: faz a seção ser "colapsável"
        }),
    )
    readonly_fields = ('data_pedido', 'total') # Campos que não podem ser editados

# Se você ainda não registrou, faça isso:
@admin.register(EnderecoEntrega)
class EnderecoEntregaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rua', 'cidade', 'estado', 'cep')
    search_fields = ('usuario__username', 'cidade', 'cep')

@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    list_editable = ('ativo',)

# Você pode ter outros registros de admin aqui, como ProdutoAdmin, MarcaAdmin, CategoriaAdmin
# admin.site.register(Produto)
# admin.site.register(Marca)
# admin.site.register(Categoria)