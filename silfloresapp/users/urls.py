from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update/', views.user_update, name='update'),
    path('<str:username>/', views.user_profile, name='profile'),
    path('delete/', views.user_delete, name='delete'),
]