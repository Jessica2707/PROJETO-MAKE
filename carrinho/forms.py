from django import forms
from .models import ItemCarrinho
from .models import Carrinho, ItemCarrinho


class ItemCarrinhoForm(forms.ModelForm):
    class Meta:
        model = ItemCarrinho
        fields = ['produto', 'quantidade']