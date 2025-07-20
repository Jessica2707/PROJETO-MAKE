from django.shortcuts import render, get_object_or_404, redirect
from .models import Produto
from .forms import ProdutoForm
from .models import Pedido
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Marca
from .forms import MarcaForm
from .models import Categoria
from .forms import CategoriaForm
from .forms import PedidoForm

def home(request):
    return render(request, 'produtos/home.html')

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'listar_produtos.html', {'produtos': produtos})

def produto_create(request):
    form = ProdutoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('produto_list')
    return render(request, 'produto/produto_form.html', {'form': form})

def produto_update(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(request.POST or None, instance=produto)
    if form.is_valid():
        form.save()
        return redirect('produto_list')
    return render(request, 'produto/produto_form.html', {'form': form})

def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('produto_list')
    return render(request, 'produto/produto_confirm_delete.html', {'produto': produto})

def ver_carrinho(request):
    return render(request, 'carrinho/ver_carrinho.html')  # ajuste o caminho do template conforme necessário

def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    carrinho = request.session.get('carrinho', {})
    
    if str(produto_id) in carrinho:
        carrinho[str(produto_id)] += 1
    else:
        carrinho[str(produto_id)] = 1

    request.session['carrinho'] = carrinho
    return redirect('listar_produtos')

from django.shortcuts import redirect

def excluir_item_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})

    # Verifica se o produto está no carrinho
    produto_id_str = str(produto_id)
    if produto_id_str in carrinho:
        del carrinho[produto_id_str]  # remove o item
        request.session['carrinho'] = carrinho  # atualiza a sessão

    return redirect('ver_carrinho')  # redireciona para a visualização do carrinho

def incluir_produto_no_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    # Recupera o carrinho da sessão (ou cria um vazio se não existir)
    carrinho = request.session.get('carrinho', {})

    # Converte o ID para string (já que session usa str como chave)
    produto_id_str = str(produto_id)

    # Se o produto já estiver no carrinho, incrementa a quantidade
    if produto_id_str in carrinho:
        carrinho[produto_id_str] += 1
    else:
        carrinho[produto_id_str] = 1

    # Atualiza a sessão com o novo carrinho
    request.session['carrinho'] = carrinho

def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})

    produto_id_str = str(produto_id)
    if produto_id_str in carrinho:
        del carrinho[produto_id_str]
        request.session['carrinho'] = carrinho

    return redirect('ver_carrinho')

def incluir_produto_no_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    carrinho = request.session.get('carrinho', {})

    produto_id_str = str(produto_id)
    if produto_id_str in carrinho:
        carrinho[produto_id_str] += 1
    else:
        carrinho[produto_id_str] = 1

    request.session['carrinho'] = carrinho

    return redirect('ver_carrinho') 

def pedido_realizado(request):
    return render(request, 'pedido/pedido_realizado.html')

def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'pedidos.html', {'pedidos': pedidos})
def finalizar_pedido(request):
    # Aqui você pode implementar a lógica de finalização do pedido
    # Exemplo: limpar o carrinho da sessão
    request.session['carrinho'] = {}

    # Redireciona para uma página de confirmação
    return redirect('pedido_realizado')

def detalhes_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedido/detalhes_pedido.html', {'pedido': pedido})

def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # ou qualquer outra página após o cadastro
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

def detalhe_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'produto/detalhe_produto.html', {'produto': produto})

def listar_marcas(request):
    marcas = Marca.objects.all()
    return render(request, 'produtos/admin/marca/listar.html', {'marcas': marcas})

def criar_marca(request):
    form = MarcaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_marcas')
    return render(request, 'produtos/admin/marca/criar.html', {'form': form})

def editar_marca(request, id):
    marca = get_object_or_404(Marca, id=id)
    form = MarcaForm(request.POST or None, instance=marca)
    if form.is_valid():
        form.save()
        return redirect('listar_marcas')
    return render(request, 'produtos/admin/marca/editar.html', {'form': form, 'marca': marca})

def deletar_marca(request, id):
    marca = get_object_or_404(Marca, id=id)
    if request.method == 'POST':
        marca.delete()
        return redirect('listar_marcas')
    return render(request, 'produtos/admin/marca/confirmar_delete.html', {'marca': marca})

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('listar_produtos')

    return render(request, 'produtos/editar.html', {'form': form, 'produto': produto})

def deletar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('listar_produtos')

def listar_produtos_admin(request):
    produtos = Produto.objects.all()
    return render(request, 'admin/listar_produtos.html', {'produtos': produtos})

def criar_produto(request):
    form = ProdutoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('listar_produtos')
    return render(request, 'produtos/admin/criar.html', {'form': form})

def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    carrinho_itens = []
    total = 0

    for produto_id, quantidade in carrinho.items():
        produto = Produto.objects.get(id=produto_id)
        subtotal = produto.preco * quantidade
        total += subtotal
        carrinho_itens.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal,
        })

    return render(request, 'carrinho.html', {'carrinho_itens': carrinho_itens, 'total': total})

def finalizar_compra(request):
    carrinho = request.session.get('carrinho', {})
    if request.method == 'POST':
        # Aqui você pode salvar o pedido e limpar o carrinho
        request.session['carrinho'] = {}
        return redirect('home')

    carrinho_itens = []
    total = 0
    for produto_id, quantidade in carrinho.items():
        produto = Produto.objects.get(id=produto_id)
        subtotal = produto.preco * quantidade
        total += subtotal
        carrinho_itens.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal,
        })

    return render(request, 'finalizar_compra.html', {
        'carrinho_itens': carrinho_itens,
        'total': total
    })

def resumo_pedido(request):
    # aqui monta o resumo final do pedido
    return render(request, 'resumo_pedido.html')

def pedidos(request):
    # Você pode buscar os pedidos do usuário aqui, se quiser
    return render(request, 'pedidos.html')

def detalhes_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'detalhes_pedido.html', {'pedido': pedido})

def carrinho(request):
    carrinho = request.session.get('carrinho', {})
    carrinho_itens = []
    total = 0

    for produto_id, quantidade in carrinho.copy().items():
        try:
            produto = Produto.objects.get(id=produto_id)
            subtotal = produto.preco * quantidade
            total += subtotal
            carrinho_itens.append({
                'produto': produto,
                'quantidade': quantidade,
                'subtotal': subtotal,
            })
        except ObjectDoesNotExist:
            # remove produto apagado do carrinho
            carrinho.pop(str(produto_id))
            request.session['carrinho'] = carrinho  # atualiza a sessão

    return render(request, 'carrinho.html', {
        'carrinho_itens': carrinho_itens,
        'total': total
    })

def produto_create(request):
    form = ProdutoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('listar_produtos')
    return render(request, 'produtos/admin/criar.html', {'form': form})

def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'produtos/cliente/meus_pedidos.html', {'pedidos': pedidos})

def detalhes_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'produtos/cliente/detalhes_pedido.html', {'pedido': pedido})



def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'produtos/admin/categoria/listar.html', {'categorias': categorias})

def criar_categoria(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_categorias')
    return render(request, 'produtos/admin/categoria/criar.html', {'form': form})

def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect('listar_categorias')
    return render(request, 'produtos/admin/categoria/editar.html', {'form': form, 'categoria': categoria})

def deletar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'produtos/admin/categoria/confirmar_delete.html', {'categoria': categoria})

def finalizar_pedido(request):
    form = PedidoForm(request.POST or None)
    if form.is_valid():
        pedido = form.save(commit=False)
        pedido.usuario = request.user
        pedido.save()
        return redirect('pedido_realizado')
    return render(request, 'pedidos/finalizar.html', {'form': form})