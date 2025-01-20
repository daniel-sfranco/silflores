from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib.auth import login, logout
from cart.models import Cart
from django.core.mail import EmailMessage

# Create your views here.

def user_register(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            user.cart = Cart(user=user, status="open")
            user.cart.save()
            login(request, user)
            if(next_url):
                return HttpResponseRedirect(next_url)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/user_register.html', {"form":form, "next":next_url})


def user_login(request):
    if request.method == "POST":
        next_url = request.GET.get('next') or request.POST.get('next')
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if next_url:
                return HttpResponseRedirect(next_url)
            return redirect('home')
        else:
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return HttpResponseRedirect(f"{request.path}?next={next_url}")
            return HttpResponseRedirect(f"{request.path}")
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

def user_profile(request, username):
    user = CustomUser.objects.get(username=username)
    return render(request, 'users/user_profile.html', {'profile': user})

def user_delete(request):
    user = CustomUser.objects.get(username = request.user.username)
    cart = user.cart
    if user.is_authenticated:
        logout(request)
    cart.delete()
    user.delete()
    return redirect('home')



class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset_form.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
