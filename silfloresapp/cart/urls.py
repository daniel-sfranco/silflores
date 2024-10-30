from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('', views.cart_page, name='page'),
    path('<slug:slug>/add', views.cart_add, name='add'),
    path('<slug:slug>/deleteItem', views.cart_deleteItem, name='deleteItem'),
]