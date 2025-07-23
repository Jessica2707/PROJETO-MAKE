from django.contrib import admin
from .models import Carrinho, ItemCarrinho


@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'data_criacao', 'atualizado_em']
    list_filter = ['usuario']

@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ['carrinho', 'produto', 'quantidade']
    list_filter = ['carrinho', 'produto']
