from django.contrib.auth import views as auth_views #type:ignore
from django.shortcuts import render, redirect, HttpResponseRedirect #type:ignore
from django.contrib.auth.forms import AuthenticationForm #type:ignore
from django.urls import reverse #type:ignore
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib.auth import login, logout #type:ignore
from cart.models import Cart
from django.core.mail import EmailMessage #type:ignore
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_register(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if(form.is_valid()):
            user = form.save(commit=False)
            if(not user.phone.isnumeric()):
                newPhone = []
                for c in user.phone:
                    if c.isnumeric:
                        newPhone.append(c)
                user.phone = "".join(newPhone)
            user.save()
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

@login_required(login_url="/user/login")
def user_update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/user_update.html', {"form": form})

@login_required(login_url="/user/login")
def user_profile(request, username):
    user = CustomUser.objects.get(username=username)
    return render(request, 'users/user_profile.html', {'profile': user})

@login_required(login_url="/user/login")
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
