from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import CustomUser
from .models import Cart, CartItem
from products.models import Product
from django.utils import timezone
# Create your views here.

@login_required(login_url="/user/login")
def cart_page(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'cart/cart_page.html', {'user': request.user, 'cart': cart, 'items': cart.cartitem_set.order_by('-datetime')})


@login_required(login_url='/user/login')
def cart_add(request, slug):
    cart = Cart.objects.get(user=request.user)
    product = Product.objects.get(slug=slug)
    cartItem = CartItem.objects.filter(product=product).filter(cart=cart)
    if cartItem:
        cartItem[0].quantity += 1
        cartItem[0].fullPrice += product.price
        cartItem[0].datetime = timezone.now()
        cartItem[0].save()
    else:
        cartItem = CartItem(product=product, cart=cart, quantity=1, itemName=f"{request.user.username}_{product.slug}", fullPrice=product.price)
        cartItem.save()
    cart.products += 1
    cart.fullPrice += product.price
    cart.save()
    if(product.stock > 0):
        product.stock -= 1
        product.save()
    return redirect(f'/cart')

@login_required(login_url='/user/login')
def cart_deleteItem(request, slug):
    user = CustomUser.objects.get(username=request.user.username)
    cart = user.cart
    cartItem = CartItem.objects.filter(itemName=slug)[0]
    if cartItem:
        cart.fullPrice -= cartItem.fullPrice
        cart.products -= cartItem.quantity
        cartItem.delete()
        cart.save()
    return redirect('/cart')