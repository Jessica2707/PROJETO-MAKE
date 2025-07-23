"""
URL configuration for make project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from produtos.admin import admin_site
from produtos import views
from django.urls import include
from produtos.views import listar_categorias




urlpatterns = [
    path('', views.home, name='home'),
    path('', include('produtos.urls')),
    path('admin/', admin_site.urls),
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('login/', auth_views.LoginView.as_view(template_name='produtos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('pedido-realizado/', views.pedido_realizado, name='pedido_realizado'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('pedido/<int:pedido_id>/', views.detalhes_pedido, name='detalhes_pedido'),
    path('cadastro/', views.registrar_usuario, name='cadastro'),
    path('produto/<int:produto_id>/', views.detalhe_produto, name='detalhe_produto'),
    path('marcas/editar/<int:id>/', views.editar_marca, name='editar_marca'),
    path('marcas/deletar/<int:id>/', views.deletar_marca, name='deletar_marca'),
    path('produtos/editar/<int:id>/', views.editar_produto, name='editar'),
    path('produtos/deletar/<int:id>/', views.deletar_produto, name='deletar'),
    path('admin/produtos/', views.listar_produtos_admin, name='listar_produtos_admin'),
    path('admin/produtos/novo/', views.criar_produto, name='criar_produto'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('marcas/', views.listar_marcas, name='listar_marcas'),
    path('categorias/', listar_categorias, name='listar_categorias'),
    path('carrinho/', include('carrinho.urls')),
    path('enderecos/', include('produtos.urls')),
    path('', include('produtos.urls')),


    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)