from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name='list'),
    path('new-product/', views.product_new, name='new'),
    path('<slug:slug>', views.product_page, name='page'),
]