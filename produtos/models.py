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
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class EnderecoEntrega(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.bairro}'


# 🛍️ Pedido

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    endereco_entrega = models.ForeignKey(EnderecoEntrega, on_delete=models.SET_NULL, null=True)
    forma_pagamento_selecionada = models.ForeignKey(FormaPagamento, on_delete=models.SET_NULL, null=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Processando', 'Processando'),
        ('Enviado', 'Enviado'),
        ('Concluido', 'Concluído'),
        ('Cancelado', 'Cancelado'),
        ('Aguardando Pagamento', 'Aguardando Pagamento'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')

    def __str__(self):
        return f"Pedido #{self.pk} - {self.usuario.username}"


# 📋 Item do pedido
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE) # Seu modelo de Produto
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Preço no momento da compra

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome} ({self.pedido.pk})"

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario


# 🏷️ Estoque
class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.produto.nome}: {self.quantidade} unid."

class ItemCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    adicionado_em = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.produto.preco * self.quantidade

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"




