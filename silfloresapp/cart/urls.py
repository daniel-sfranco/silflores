from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('<str:username>/page', views.cart_page, name='page'),
    path('add', views.cart_add, name='add'),
    path('<str:pk>/deleteItem', views.cart_deleteItem, name='deleteItem'),
    path('orders/all', views.cart_orders, name='orders'),
    path('<str:username>/messages', views.get_messages, name='messages'),
    path('setQuantity', views.set_quantity, name='quantity'),
    path('<str:username>/processPayment', views.process_payment, name='processPayment'),
    path("pagseguro/notification/", views.notification_handler, name="pagseguro_notification"),
    path('<str:username>/confirm/', views.confirm_purchase, name='confirm'),
    path('thanks', views.thanks, name='thanks'),
    path('<str:username>/getTicket', views.get_ticket, name='getTicket'),
    path('<str:username>/setSent', views.set_sent, name='setSent'),
    path('<str:username>/track', views.track_shipment, name='trackShipment'),
]
