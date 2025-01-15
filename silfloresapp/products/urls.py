from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_collections, name='collections'),
    path('<str:tagName>/list', views.products_list, name='list'),
    path('<str:tagName>/list/<str:searchTerm>', views.products_list, name='list'),
    path('new-product/', views.product_new, name='new'),
    path('<slug:slug>', views.product_page, name='page'),
    path('<slug:slug>/delete', views.product_delete, name='delete'),
    path('<slug:slug>/update', views.product_update, name='update'),
    path('photo/<str:pk>/delete', views.photo_delete, name='delete_photo'),
]