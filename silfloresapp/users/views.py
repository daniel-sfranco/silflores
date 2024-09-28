from django.shortcuts import render

# Create your views here.

def user_register(request):
    return render(request, 'users/user_register.html')

def user_login(request):
    return render(request, 'users/user_login.html')
