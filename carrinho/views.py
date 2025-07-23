from django.shortcuts import render, get_object_or_404, redirect
from .models import Carrinho, ItemCarrinho
from .forms import ItemCarrinhoForm
from produtos.models import Produto
from carrinho.models import Carrinho, ItemCarrinho

# 🛒 Listar todos os itens do carrinho do cliente atual
def listar_carrinho(request):
    carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
    itens = ItemCarrinho.objects.filter(carrinho=carrinho)
    return render(request, 'carrinho/listar.html', {'itens': itens})


# ➕ Adicionar produto ao carrinho via formulário
def adicionar_item_carrinho(request):
    form = ItemCarrinhoForm(request.POST or None)
    if form.is_valid():
        item = form.save(commit=False)
        carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
        item.carrinho = carrinho
        item.save()
        return redirect('listar_carrinho')
    return render(request, 'carrinho/adicionar.html', {'form': form})


# ✏️ Editar quantidade de um item do carrinho
def editar_item_carrinho(request, id):
    item = get_object_or_404(ItemCarrinho, id=id)
    form = ItemCarrinhoForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('listar_carrinho')
    return render(request, 'carrinho/editar.html', {'form': form})

# ❌ Remover item do carrinho
def remover_item_carrinho(request, id):
    item = get_object_or_404(ItemCarrinho, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('listar_carrinho')
    return render(request, 'carrinho/remover.html', {'item': item})
