import json
import requests #type:ignore
from django.http import HttpResponse, JsonResponse#type:ignore
from django.urls import reverse#type:ignore
from django.shortcuts import render, redirect#type:ignore
from django.contrib.auth.decorators import login_required, user_passes_test#type:ignore
from users.models import CustomUser
from .models import Cart, CartItem, Message
from products.models import Product, Photo
from django.utils import timezone#type:ignore
from .pagseguro_service import PagSeguroAPI
from django.conf import settings#type:ignore
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
    quantity = 1
    product = Product.objects.get(slug=slug)
    cartItem = CartItem.objects.filter(product=product).filter(cart=cart)
    if cartItem:
        quantity
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


def set_quantity(request):
    data = json.loads(request.body)
    pk = data['pk']
    quantity = int(data['quantity'])
    cartItem = CartItem.objects.get(pk=pk)
    cart = cartItem.cart
    actQuantity = cartItem.quantity
    difQuantity = quantity - actQuantity
    cartItem.quantity += difQuantity
    cart.products += difQuantity
    cartItem.fullPrice += difQuantity * cartItem.product.price
    cart.fullPrice += difQuantity * cartItem.product.price
    cartItem.save()
    cart.save()
    return JsonResponse({"message": "Success"})


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
    return redirect(f'/cart/{request.user.username}/page')


@login_required(login_url='/user/login')
@user_passes_test(lambda u: u.is_superuser)
def cart_orders(request):
    superusers = CustomUser.objects.filter(is_superuser=True)
    carts = Cart.objects.exclude(products=0).exclude(user__in=superusers)
    carts_items = {}
    for cart in carts:
        carts_items[cart.id] = cart.cartitem_set.order_by("-datetime")
    return render(request, 'cart/cart_visualization.html', {'carts':carts, 'items':carts_items})


def get_messages(request, username):
    cart = Cart.objects.get(user__username=username)
    messagesQuery = Message.objects.filter(cart=cart).order_by("datetime")
    messagesData = []
    for message in messagesQuery:
        messagesData.append({
            'content': message.content,
            'sender': message.sender.username,
            'date': f'{message.datetime.day}/{message.datetime.month}/{message.datetime.year}',
            'time': f'{message.datetime.hour}:{message.datetime.minute}'
        })
    return JsonResponse({'messages': messagesData, 'length': len(messagesData)})


def process_payment(request, username):
    if request.method == "POST":
        cart = Cart.objects.get(user__username=username)
        user = cart.user
        cep = user.cep.replace("-", "")
        address = requests.get(f"https://viacep.com.br/ws/{cep}/json").json()
        data = {
            "customer": {
                "phone": {
                    "country": "+55",
                    "area": str(user.ddd),
                    "number": str(user.phone),
                },
                "Name": user.name,
                "email": user.email,
                "tax_id": user.cpf,
            },
            "shipping": {
                "address": {
                    "street": address["logradouro"],
                    "number": str(user.home_number),
                    "city": address["localidade"],
                    "region_code": address["uf"],
                    "country": "BRA",
                    "postal_code": user.cep,
                    "complement": user.complement,
                    "locality": address["bairro"]
                },
                "box": {
                    "dimensions": {
                        "length": 16,
                        "width": 11,
                        "height": 3
                    },
                    "weight": 300
                },
                "type": "FIXED",
                "address_modifiable": False,
                "amount": 0 if settings.PAGSEGURO_SANDBOX else 0 #implementar melhor envio posteriormente, 0 para testes
            },
            "customer_modifiable": True,
            "reference_id": cart.id,
            "items": [],
            "payment_methods": [{ "type": "CREDIT_CARD" }, { "type": "DEBIT_CARD" }, { "type": "BOLETO" }, { "type": "PIX" }],
            "redirect_url": "https://pagseguro.uol.com.br"
        }
        for cartitem in cart.cartitem_set.all():
            item = {}
            item['reference_id'] = cartitem.product.id
            item['name'] = cartitem.product.name
            item['quantity'] = cartitem.quantity
            item['unit_amount'] = int(cartitem.product.price * 100)
            data['items'].append(item)
        response = PagSeguroAPI.generate_payment(data)
        for item in response['links']:
            if item['rel'] == 'PAY':
                print(item['href'])
    return JsonResponse(data={}, status=500)


def notification_handler(request):
    if request.method == "POST":
        notification_code = request.POST.get("notificationCode")
        notification_type = request.POST.get("notificationType")

        if notification_type == "transaction":
            transaction_details = PagSeguroAPI.get_transaction_details(notification_code)
            print(transaction_details)

    return HttpResponse(status=200)