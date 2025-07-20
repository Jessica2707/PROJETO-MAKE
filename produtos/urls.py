from django.urls import path
from produtos import views
from .views import listar_marcas, criar_marca, editar_marca, deletar_marca
from .views import listar_categorias, criar_categoria, editar_categoria, deletar_categoria

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('produtos/criar/', views.produto_create, name='produto_create'),
    path('produtos/<int:pk>/editar/', views.produto_update, name='produto_update'),
    path('produtos/<int:pk>/excluir/', views.produto_delete, name='produto_delete'),
    
    # Carrinho
    path('carrinho/', views.carrinho, name='carrinho'),  # só essa com name='carrinho'
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<int:produto_id>/', views.excluir_item_carrinho, name='remover_do_carrinho'),

    # Pedido
    path('finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('pedido/resumo/', views.resumo_pedido, name='resumo_pedido'),
    path('pedido-realizado/', views.pedido_realizado, name='pedido_realizado'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('pedido/<int:pedido_id>/', views.detalhes_pedido, name='detalhes_pedido'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('pedido/<int:pedido_id>/', views.detalhes_pedido, name='detalhes_pedido'),

    # Produtos (detalhes e marcas)
    path('produto/<int:produto_id>/', views.detalhe_produto, name='detalhe_produto'),
    path('marcas/', listar_marcas, name='listar_marcas'),
    path('marcas/criar/', criar_marca, name='criar_marca'),
    path('marcas/<int:id>/editar/', editar_marca, name='editar_marca'),
    path('marcas/<int:id>/excluir/', deletar_marca, name='deletar_marca'),

    # Administração
    path('admin/produtos/', views.listar_produtos, name='listar_produtos_admin'),
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
    
]