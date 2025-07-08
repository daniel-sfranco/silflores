from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update/', views.user_update, name='updateUser'),
    path('<str:username>/profile', views.user_profile, name='profile'),
    path('delete/', views.user_delete, name='deleteUser'),
    path('reset-password/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]