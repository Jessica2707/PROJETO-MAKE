from django.urls import path
from produtos import views
from .views import listar_marcas, criar_marca, editar_marca, deletar_marca
from .views import listar_categorias, criar_categoria, editar_categoria, deletar_categoria
from .views import (
    listar_formas_pagamento,
    adicionar_forma_pagamento,
    editar_forma_pagamento,
    excluir_forma_pagamento
)
from .views import adicionar_forma_pagamento
from .views import listar_pedidos  
from .views import criar_pedido
from .views import editar_pedido
from .views import excluir_pedido
from .views import (
    ver_carrinho,
    adicionar_ao_carrinho,
    editar_item_carrinho,
    remover_item_carrinho
    
)
from .views import atualizar_quantidade
from .views import finalizar_pedido





urlpatterns = [
    path('', views.home, name='home'),
    path('admin/produtos/', views.listar_produtos_admin, name='listar_produtos_admin'),
    path('produtos/<int:pk>/editar/', views.produto_update, name='produto_update'),
    path('produtos/<int:pk>/excluir/', views.produto_delete, name='produto_delete'),
    path('admin/produtos/novo/', views.criar_produto, name='criar_produto'),
    path('carrinho/adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),


    
    

    # Pedido
    path('admin/carrinho/', views.painel_carrinho, name='painel_carrinho'),
    path('admin/pedidos/', listar_pedidos, name='listar_pedidos'),
    path('admin/pedidos/novo/', criar_pedido, name='criar_pedido'),
    path('admin/pedidos/<int:id>/editar/', editar_pedido, name='editar_pedido'),
    path('admin/pedidos/<int:id>/excluir/', excluir_pedido, name='excluir_pedido'),
    path('admin/pedidos/pagamento/', views.pagina_pagamento, name='pagina_pagamento'),
    path('finalizar/', finalizar_pedido, name='finalizar_pedido'),




    # Produtos (detalhes e marcas)
    path('marcas/', listar_marcas, name='listar_marcas'),
    path('marcas/criar/', criar_marca, name='criar_marca'),
    path('marcas/<int:id>/editar/', editar_marca, name='editar_marca'),
    path('marcas/<int:id>/excluir/', deletar_marca, name='deletar_marca'),

    # Administração
    path('admin/produtos/novo/', views.criar_produto, name='criar_produto'),

    # Outras rotas
    path('cadastro/', views.registrar_usuario, name='cadastro'),
    path('listar/', views.listar_produtos, name='listar_produtos'),
    path('editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('deletar/<int:id>/', views.deletar_produto, name='deletar_produto'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),

    # Categoria
    path('categorias/', listar_categorias, name='listar_categorias'),
    path('categorias/criar/', criar_categoria, name='criar_categoria'),
    path('categorias/<int:id>/editar/', editar_categoria, name='editar_categoria'),
    path('categorias/<int:id>/excluir/', deletar_categoria, name='deletar_categoria'),

    
    #endereço
    path('enderecos/', views.listar_enderecos, name='listar_enderecos'),
    path('enderecos/novo/', views.adicionar_endereco, name='adicionar_endereco'),
    path('enderecos/<int:pk>/editar/', views.editar_endereco, name='editar_endereco'),
    path('enderecos/<int:pk>/excluir/', views.excluir_endereco, name='excluir_endereco'),

    # Pagamento
    path('pagamento/', views.listar_formas_pagamento, name='listar_formas_pagamento'),
    path('pagamento/nova/', adicionar_forma_pagamento, name='adicionar_forma_pagamento'),
    path('pagamento/<int:pk>/editar/', editar_forma_pagamento, name='editar_forma_pagamento'),
    path('pagamento/<int:pk>/excluir/', excluir_forma_pagamento, name='excluir_forma_pagamento'),
    path('pagamento/nova/', adicionar_forma_pagamento, name='adicionar_forma_pagamento'),
    path('pagamento/nova/', views.nova_forma_pagamento, name='adicionar_forma_pagamento'),


    #carrinho
    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/editar/<int:id>/', editar_item_carrinho, name='editar_item_carrinho'),
    path('carrinho/remover/<int:id>/', remover_item_carrinho, name='remover_item_carrinho'),
    path('carrinho/atualizar/<int:id>/', atualizar_quantidade, name='atualizar_quantidade'),




    # URLs de Checkout e Finalização
    path('checkout/', views.checkout, name='checkout'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    
    # Outras URLs necessárias para o gateway de pagamento (ex: callbacks de retorno)
]