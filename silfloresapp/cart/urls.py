from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('', views.cart_page, name='page'),
    path('add', views.cart_add, name='add'),
    path('<slug:slug>/deleteItem', views.cart_deleteItem, name='deleteItem'),
    path('orders', views.cart_orders, name='orders'),
]