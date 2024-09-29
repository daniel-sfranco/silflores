from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login

# Create your views here.

def user_register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            login(request, form.save())
            return redirect('products:list')
    else:
        form = UserCreationForm()
    return render(request, 'users/user_register.html', {"form":form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('products:list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/user_login.html', {"form":form})
