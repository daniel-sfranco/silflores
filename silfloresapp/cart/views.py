import json
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import CustomUser
from .models import Cart, CartItem, Message
from products.models import Product
from django.utils import timezone
# Create your views here.

@login_required(login_url="/user/login")
def cart_page(request, username):
    cart = Cart.objects.get(user__username=username)
    items = [cartitem for cartitem in cart.cartitem_set.order_by('-product__name')]
    cartUser = {'name': cart.user.name, 'username': cart.user.username}
    user = CustomUser.objects.get(username=request.user.username)
    return render(request, 'cart/cart_page.html', {'cartUser': cartUser, 'cart': cart, 'items': items, 'user': user, 'messages': Message.objects.filter(cart=cart).order_by("datetime")})


@login_required(login_url='/user/login')
def cart_add(request):
    if not request.user.is_authenticated:
        next_url = request.META.get('HTTP_REFERER') or request.path
        return JsonResponse({'redirect': reverse('login') + "?next=" + next_url})
    cart = Cart.objects.get(user=request.user)
    data = json.loads(request.body)
    slug = data['slug']
    quantity = int(data['quantity'])
    product = Product.objects.get(slug=slug)
    cartItem = CartItem.objects.filter(product=product).filter(cart=cart)
    if cartItem:
        cartItem[0].quantity += quantity
        cartItem[0].fullPrice += product.price * quantity
        cartItem[0].datetime = timezone.now()
        cartItem[0].save()
    else:
        cartItem = CartItem(product=product, cart=cart, quantity=quantity, itemName=f"{request.user.username}_{product.slug}", fullPrice=product.price * quantity)
        cartItem.save()
    cart.products += quantity
    cart.fullPrice += product.price * quantity
    cart.save()
    product.stock = max(product.stock - quantity, 0)
    product.save()
    return HttpResponse("Product correctly added to cart")


@login_required(login_url='/user/login')
def cart_deleteItem(request, pk):
    user = CustomUser.objects.get(username=request.user.username)
    cart = user.cart
    cartItem = CartItem.objects.get(pk=pk)
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
