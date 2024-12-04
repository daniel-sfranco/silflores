import json
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
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
def cart_add(request):
    if not request.user.is_authenticated:
        next_url = request.META.get('HTTP_REFERER') or request.path
        return JsonResponse({'redirect': reverse('users:login') + "?next=" + next_url})
    cart = Cart.objects.get(user=request.user)
    data = json.loads(request.body)
    slug = data['slug']
    size = data['size']
    quantity = data['quantity']
    product = Product.objects.get(slug=slug)
    cartItem = CartItem.objects.filter(product=product).filter(cart=cart).filter(size=size)
    if cartItem:
        cartItem[0].quantity += quantity
        cartItem[0].fullPrice += product.price * quantity
        cartItem[0].datetime = timezone.now()
        cartItem[0].save()
    else:
        cartItem = CartItem(product=product, cart=cart, quantity=quantity, itemName=f"{request.user.username}_{product.slug}", fullPrice=product.price * quantity, sizeType=product.size_type, size=size)
        cartItem.save()
    cart.products += quantity
    cart.fullPrice += product.price * quantity
    cart.save()
    if(product.stock > quantity):
        product.stock -= quantity
    else:
        product.stock = 0
    product.save()
    return HttpResponse("Product correctly added to cart")


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


@login_required(login_url='/user/login')
@user_passes_test(lambda u: u.is_superuser)
def cart_orders(request):
    superusers = CustomUser.objects.filter(is_superuser=True)
    carts = Cart.objects.exclude(products=0).exclude(user__in=superusers)
    carts_items = {}
    for cart in carts:
        carts_items[cart.id] = cart.cartitem_set.order_by("-datetime")
    return render(request, 'cart/cart_visualization.html', {'carts':carts, 'items':carts_items})
