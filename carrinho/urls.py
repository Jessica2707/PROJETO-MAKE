from django.urls import path
from . import views


urlpatterns = [
path('', views.listar_carrinho, name='listar_carrinho'),
path('adicionar/', views.adicionar_item_carrinho, name='adicionar_item_carrinho'),
path('<int:id>/editar/', views.editar_item_carrinho, name='editar_item_carrinho'),
path('<int:id>/remover/', views.remover_item_carrinho, name='remover_item_carrinho'),

]


