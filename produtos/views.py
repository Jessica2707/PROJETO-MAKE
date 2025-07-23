from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm

from .models import Produto, Pedido, Marca, Categoria
from .forms import ProdutoForm, MarcaForm, CategoriaForm, PedidoForm

from carrinho.models import Carrinho
from .forms import EnderecoEntregaForm
from .models import EnderecoEntrega
from .models import FormaPagamento
from .forms import FormaPagamentoForm
from django.contrib.auth.decorators import login_required
from .models import ItemCarrinho
from carrinho.views import editar_item_carrinho






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

@login_required
def ver_carrinho(request):
    itens = ItemCarrinho.objects.filter(usuario=request.user)
    total = sum(item.subtotal() for item in itens)
    return render(request, 'carrinho/lista.html', {'itens': itens, 'total': total})

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    quantidade = int(request.POST.get('quantidade', 1))
    item, criado = ItemCarrinho.objects.get_or_create(usuario=request.user, produto=produto)
    if not criado:
        item.quantidade += quantidade
    else:
        item.quantidade = quantidade
    item.save()
    return redirect('ver_carrinho')

@login_required
def editar_item_carrinho(request, id):
    item = get_object_or_404(ItemCarrinho, id=id, usuario=request.user)
    if request.method == 'POST':
        nova_qtd = int(request.POST.get('quantidade', 1))
        item.quantidade = nova_qtd
        item.save()
        return redirect('ver_carrinho')
    return render(request, 'carrinho/editar_item.html', {'item': item})

@login_required
def remover_item_carrinho(request, id):
    item = get_object_or_404(ItemCarrinho, id=id, usuario=request.user)
    item.delete()
    return redirect('ver_carrinho')

@login_required
def atualizar_quantidade(request, id):
    item = get_object_or_404(ItemCarrinho, id=id, usuario=request.user)
    if request.method == 'POST':
        nova_qtd = int(request.POST.get('quantidade', 1))
        item.quantidade = nova_qtd
        item.save()
    return redirect('ver_carrinho')




def pedido_realizado(request):
    return render(request, 'pedido/pedido_realizado.html')

def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'pedidos.html', {'pedidos': pedidos})
@login_required
def finalizar_pedido(request):
    itens = ItemCarrinho.objects.filter(usuario=request.user)

    if not itens.exists():
        messages.error(request, "O carrinho está vazio 😢")
        return redirect('ver_carrinho')

    pedido = Pedido.objects.create(
        usuario=request.user,
        endereco=request.POST.get('endereco'),
        forma_pagamento=request.POST.get('forma_pagamento'),
        total=sum(item.subtotal() for item in itens)
    )

    for item in itens:
        PedidoItem.objects.create(
            pedido=pedido,
            produto=item.produto,
            quantidade=item.quantidade,
            subtotal=item.subtotal()
        )

    itens.delete()

    messages.success(request, "Pedido confirmado com sucesso 💖")
    return redirect('pedidos_usuario')

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
    return render(request, 'admin/listar_marcas.html', {'marcas': marcas})

def criar_marca(request):
    form = MarcaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_marcas')
    return render(request, 'admin/criar_marca.html', {'form': form})

def editar_marca(request, id):
    marca = get_object_or_404(Marca, id=id)
    form = MarcaForm(request.POST or None, instance=marca)
    if form.is_valid():
        form.save()
        return redirect('listar_marcas')
    return render(request, 'admin/editar_marca.html', {'form': form, 'marca': marca})

def deletar_marca(request, id):
    marca = get_object_or_404(Marca, id=id)
    if request.method == 'POST':
        marca.delete()
        return redirect('listar_marcas')
    return render(request, 'admin/excluir_marca.html', {'marca': marca})

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
        return redirect('listar_produtos_admin')  # ou 'listar_produtos'
    return render(request, 'admin/criar_produto.html', {'form': form})



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
    return render(request, 'admin/listar_categorias.html', {'categorias': categorias})

def criar_categoria(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_categorias')
    return render(request, 'admin/criar_categoria.html', {'form': form})

def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect('listar_categorias')
    return render(request, 'admin/editar_categoria.html', {'form': form, 'categoria': categoria})

def deletar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'admin/excluir_categoria.html', {'categoria': categoria})

def finalizar_pedido(request):
    form = PedidoForm(request.POST or None)
    if form.is_valid():
        pedido = form.save(commit=False)
        pedido.usuario = request.user
        pedido.save()
        return redirect('pedido_realizado')
    return render(request, 'pedidos/finalizar.html', {'form': form})


@login_required(login_url='/login/')
def ver_carrinho(request):
    itens = ItemCarrinho.objects.filter(usuario=request.user)
    total = sum(item.subtotal() for item in itens)
    return render(request, 'carrinho/ver_carrinho.html', {'itens': itens, 'total': total})

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    item, created = ItemCarrinho.objects.get_or_create(
        produto=produto, usuario=request.user,
        defaults={'quantidade': 1}
    )
    if not created:
        item.quantidade += 1
        item.save()
    return redirect('ver_carrinho')


@login_required
def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, usuario=request.user)
    item.delete()
    return redirect('ver_carrinho')

@login_required
def atualizar_quantidade(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, usuario=request.user)
    if request.method == 'POST':
        nova_qtd = int(request.POST.get('quantidade'))
        item.quantidade = nova_qtd
        item.save()
    return redirect('ver_carrinho')


def adicionar_item(request):
    if request.method == 'POST':
        form = CarrinhoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_carrinho')
    else:
        form = CarrinhoForm()
    return render(request, 'carrinho/adicionar.html', {'form': form})

def editar_item(request, id):
    item = get_object_or_404(Carrinho, id=id)
    form = CarrinhoForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('listar_carrinho')
    return render(request, 'carrinho/editar.html', {'form': form})

def remover_item(request, id):
    item = get_object_or_404(Carrinho, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('listar_carrinho')
    return render(request, 'carrinho/remover.html', {'item': item})

def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'admin/listar_pedidos.html', {'pedidos': pedidos})

def criar_pedido(request):
    form = PedidoForm(request.POST or None)
    if form.is_valid():
        pedido = form.save(commit=False)
        pedido.total = 0.00  # ou calcular o total baseado no carrinho
        pedido.save()
        return redirect('listar_pedidos')
    return render(request, 'admin/criar_pedido.html', {'form': form})


def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    form = PedidoForm(request.POST or None, instance=pedido)
    if form.is_valid():
        form.save()
        return redirect('listar_pedidos')
    return render(request, 'admin/editar_pedido.html', {'form': form, 'pedido': pedido})

def excluir_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')
    return render(request, 'admin/excluir_pedido.html', {'pedido': pedido})


@login_required
def listar_enderecos(request):
    enderecos = EnderecoEntrega.objects.filter(usuario=request.user)
    return render(request, 'enderecos/listar.html', {'enderecos': enderecos})

def adicionar_endereco(request):
    form = EnderecoEntregaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        endereco = form.save(commit=False)
        endereco.usuario = request.user
        endereco.save()
        return redirect('listar_enderecos')
    return render(request, 'enderecos/form.html', {'form': form})

def editar_endereco(request, pk):
    endereco = get_object_or_404(EnderecoEntrega, pk=pk, usuario=request.user)
    form = EnderecoEntregaForm(request.POST or None, instance=endereco)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('listar_enderecos')
    return render(request, 'enderecos/form.html', {'form': form})

def excluir_endereco(request, pk):
    endereco = get_object_or_404(EnderecoEntrega, pk=pk, usuario=request.user)
    if request.method == 'POST':
        endereco.delete()
        return redirect('listar_enderecos')
    return render(request, 'enderecos/confirmar_exclusao.html', {'endereco': endereco})

def listar_formas_pagamento(request):
    formas_pagamento = FormaPagamento.objects.all()
    return render(request, 'pagamento/pagamento.html', {'formas_pagamento': formas_pagamento})


def adicionar_forma_pagamento(request):
    form = FormaPagamentoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('listar_formas_pagamento')
    return render(request, 'pagamento/form.html', {'form': form})

def editar_forma_pagamento(request, pk):
    forma = get_object_or_404(FormaPagamento, pk=pk)
    form = FormaPagamentoForm(request.POST or None, instance=forma)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('listar_formas_pagamento')
    return render(request, 'pagamento/form.html', {'form': form})

def excluir_forma_pagamento(request, pk):
    forma = get_object_or_404(FormaPagamento, pk=pk)
    if request.method == 'POST':
        forma.delete()
        return redirect('listar_formas_pagamento')
    return render(request, 'pagamento/confirmar_exclusao.html', {'forma': forma})

@login_required
def nova_forma_pagamento(request):
    if request.method == 'POST':
        form = FormaPagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_formas_pagamento')
    else:
        form = FormaPagamentoForm()
    return render(request, 'pagamento/formulario.html', {'form': form})


def checkout(request):
    itens = ItemCarrinho.objects.filter(usuario=request.user)
    total = sum(item.subtotal() for item in itens)

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.total = total
            pedido.save()
            itens.delete()
            return redirect('listar_pedidos')  # ou página de confirmação
    else:
        form = PedidoForm()

    return render(request, 'checkout.html', {'form': form, 'itens': itens, 'total': total})


def finalizar_compra(request):
    if request.method == 'POST':
        # 1. Obter os IDs selecionados do formulário
        endereco_id = request.POST.get('endereco_id')
        forma_pagamento_id = request.POST.get('forma_pagamento_id')

        # 2. Validar e obter os objetos do banco de dados
        try:
            endereco_selecionado = get_object_or_404(EnderecoEntrega, pk=endereco_id, usuario=request.user)
            forma_pagamento_selecionada = get_object_or_404(FormaPagamento, pk=forma_pagamento_id, ativo=True)
        except Exception as e:
            # Lidar com erros se o ID não for válido ou não pertencer ao usuário
            print(f"Erro ao obter endereço ou forma de pagamento: {e}")
            # Você pode adicionar uma mensagem de erro ao usuário e redirecionar de volta ao checkout
            return redirect('checkout') # ou renderizar o checkout com uma mensagem de erro

        # 3. Obter os produtos do carrinho
        produtos_carrinho = get_produtos_do_carrinho(request)
        if not produtos_carrinho:
            # Carrinho vazio, redirecionar ou mostrar mensagem
            return redirect('pagina_carrinho_vazio') # Crie uma URL e view para isso

        # 4. Calcular o total do pedido
        total_pedido = sum(item['quantidade'] * item['preco'] for item in produtos_carrinho)

        # 5. Criar o objeto Pedido
        try:
            pedido = Pedido.objects.create(
                usuario=request.user,
                endereco_entrega=endereco_selecionado,
                forma_pagamento_selecionada=forma_pagamento_selecionada,
                total=total_pedido,
                status='Pendente' # Status inicial do pedido
            )

            # 6. Criar os objetos ItemPedido para cada produto no carrinho
            for item_carrinho in produtos_carrinho:
                # É crucial que item_carrinho['objeto_produto'] seja o objeto Produto real
                # Se get_produtos_do_carrinho retorna apenas dicts, você precisará buscar o Produto:
                # produto_obj = get_object_or_404(Produto, pk=item_carrinho['id'])
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=item_carrinho['objeto_produto'], # Certifique-se que o item do carrinho inclui o objeto Produto
                    quantidade=item_carrinho['quantidade'],
                    preco_unitario=item_carrinho['preco'] # Preço do produto no momento da compra
                )

            # 7. Limpar o carrinho (Exemplo: se for baseado em sessão)
            # request.session['carrinho'] = {}
            # Ou chame uma função que limpa o carrinho:
            # clear_cart(request)

            # 8. Redirecionar para uma página de sucesso ou iniciar o fluxo do gateway de pagamento
            # Para fins de exemplo, vamos redirecionar para uma página de sucesso simples
            return redirect('pedido_confirmado', pk=pedido.pk) # Crie esta URL e view

        except Exception as e:
            # Captura qualquer erro durante a criação do pedido/itens
            print(f"Erro ao finalizar compra: {e}")
            # Adicione uma mensagem de erro ao usuário (usando Django messages, por exemplo)
            # messages.error(request, "Ocorreu um erro ao finalizar seu pedido. Tente novamente.")
            return redirect('checkout') # Redireciona de volta com erro
    else:
        # Se alguém tentar acessar /finalizar-compra/ via GET, redireciona para o checkout
        return redirect('checkout')

def pagina_pagamento(request):
    return render(request, 'admin/pedidos/pagamento.html')



@login_required
def painel_carrinho(request):
    itens = ItemCarrinho.objects.all()  # ou filtre por usuário se quiser
    total = sum(item.subtotal() for item in itens)
    return render(request, 'admin/carrinho/lista.html', {'itens': itens, 'total': total})