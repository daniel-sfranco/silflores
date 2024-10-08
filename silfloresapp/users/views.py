from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib.auth import login, logout
from django.conf import settings

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


def user_update(request):
    instance = CustomUser.objects.get(username=request.user.username)
    if request.method == "POST":
        form = CustomUserChangeForm(data=request.POST, files = request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if 'photo-clear' in request.POST:
                request.user.photo = CustomUser._meta.get_field('photo').get_default()
                request.user.save()
            return redirect('home')
    else:
        form = CustomUserChangeForm(instance=instance)
    return render(request, 'users/user_update.html', {"form": form})

def user_profile(request):
    return render(request, 'users/user_profile.html', {'profile': request.user})

def user_delete(request):
    user = CustomUser.objects.get(username = request.user.username)
    if user.is_authenticated:
        logout(request)
    user.delete()
    return redirect('home')
