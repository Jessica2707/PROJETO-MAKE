from django.db import models
from django.contrib.auth.models import User


# 👑 Administrador do sistema
class UsuarioAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_completo


# 🧴 Marca do produto
class Marca(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# 💅 Categoria do produto
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# 💄 Produto
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    cor = models.CharField(max_length=30)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome


# 👩 Cliente
class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


# 💳 Forma de pagamento
class FormaPagamento(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


# 📦 Endereço de entrega
class EnderecoEntrega(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    rua = models.CharField(max_length=150)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"


# 🛍️ Pedido

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cliente')
    endereco_entrega = models.CharField(max_length=255, verbose_name='Endereço de entrega')
    
    FORMA_PAGAMENTO_CHOICES = [
        ('pix', 'PIX'),
        ('cartao', 'Cartão de crédito'),
        ('boleto', 'Boleto bancário'),
        ('dinheiro', 'Dinheiro na entrega'),
    ]
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES,
        default='pix',
        verbose_name='Forma de pagamento'
    )

    data_pedido = models.DateTimeField(auto_now_add=True, verbose_name='Data do pedido')
    status = models.CharField(max_length=50, default='Aguardando pagamento', verbose_name='Status')

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"




# 🛒 Item do carrinho
class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey('Carrinho', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"


# 🧺 Carrinho de compras
class Carrinho(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    itens = models.ManyToManyField(Produto, through='ItemCarrinho')
    data_criacao = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrinho de {self.cliente.nome}"


# 📋 Item do pedido
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} - Pedido #{self.pedido.id}"


# 🏷️ Estoque
class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.produto.nome}: {self.quantidade} unid."



