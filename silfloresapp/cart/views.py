from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import CustomUser
from .models import Cart, CartItem

# Create your views here.

@login_required(login_url="/user/login")
def cart_page(request):
    user = CustomUser.objects.get(username=request.user.username)
    cart = user.cart
    return render(request, 'cart/cart_page.html', {'user': user, 'cart': cart, 'items': cart.cartitem_set.all()})