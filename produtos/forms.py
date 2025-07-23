from django import forms
from django.contrib.auth.models import User
from .models import Marca
from .models import Categoria
from .models import Pedido
from .models import (
    Categoria,
    Marca,
    Produto,
    EnderecoEntrega,
    FormaPagamento
)
from .models import FormaPagamento, EnderecoEntrega

# 🌸 Filtro de produtos (em listagem ou vitrine)
class FiltroProdutoForm(forms.Form):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False)
    marca = forms.ModelChoiceField(queryset=Marca.objects.all(), required=False)
    cor = forms.CharField(max_length=30, required=False)
    preco_min = forms.DecimalField(required=False, decimal_places=2, max_digits=8)
    preco_max = forms.DecimalField(required=False, decimal_places=2, max_digits=8)


# 🧾 Checkout simples
class CheckoutForm(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    endereco = forms.CharField(max_length=255)
    cidade = forms.CharField(max_length=100)
    cep = forms.CharField(max_length=20)


# 💳 Finalizar pedido (com dados reais do cliente)
class FinalizarPedidoForm(forms.Form):
    endereco = forms.ModelChoiceField(
        queryset=EnderecoEntrega.objects.none(),
        empty_label="Selecione um endereço"
    )
    forma_pagamento = forms.ModelChoiceField(
        queryset=FormaPagamento.objects.all(),
        empty_label="Selecione a forma de pagamento"
    )

    def __init__(self, cliente, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['endereco'].queryset = EnderecoEntrega.objects.filter(cliente=cliente)


# 👩 Cadastro personalizado
class FormularioCadastro(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar = cleaned_data.get("confirmar_senha")

        if senha != confirmar:
            self.add_error('confirmar_senha', "As senhas não coincidem.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['senha'])
        if commit:
            user.save()
        return user


# 📋 Pedido simples
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['usuario', 'endereco_entrega', 'forma_pagamento_selecionada', 'status']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'endereco_entrega': forms.Select(attrs={'class': 'form-select'}),
            'forma_pagamento_selecionada': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }




# 🧴 Marca
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'})
        }


# 💄 Produto
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'})
        }

class FormaPagamentoForm(forms.ModelForm):
    class Meta:
        model = FormaPagamento
        fields = ['nome', 'ativo']

class EnderecoEntregaForm(forms.ModelForm):
    class Meta:
        model = EnderecoEntrega
        fields = ['rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']


        