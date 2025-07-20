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

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'forma_pagamento']

    def data_pedido(self, obj):
        return obj.data
    

# 📝 Registro dos modelos no admin customizado
admin_site.register(Marca)
admin_site.register(Categoria)
admin_site.register(Produto, ProdutoAdmin)
admin_site.register(Cliente, ClienteAdmin)
admin_site.register(Pedido, PedidoAdmin)
admin_site.register(FormaPagamento)
admin_site.register(EnderecoEntrega)
admin_site.register(Estoque)
admin_site.register(UsuarioAdmin, UsuarioAdminInline)