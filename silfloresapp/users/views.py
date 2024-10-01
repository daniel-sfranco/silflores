from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout

# Create your views here.

def user_register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if(form.is_valid()):
            login(request, form.save())
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/user_register.html', {"form":form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/user_login.html', {"form":form})

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
