from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('<str:username>/page', views.cart_page, name='page'),
    path('add', views.cart_add, name='add'),
    path('<str:pk>/deleteItem', views.cart_deleteItem, name='deleteItem'),
    path('orders/all', views.cart_orders, name='orders'),
    path('<str:username>/messages', views.get_messages, name='messages')
]