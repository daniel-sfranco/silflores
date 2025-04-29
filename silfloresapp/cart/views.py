import json
import asyncio
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from pyppeteer import launch #type:ignore
from users.models import CustomUser
from .models import Cart, CartItem, Message, MelhorEnvioToken
from products.models import Product
from .pagseguro_service import PagSeguroAPI
from .melhorenvio_service import MelhorEnvioAPI, generate_pdf_from_url


@login_required(login_url="/user/login")
def cart_page(request, username):
    actUser = CustomUser.objects.get(username=request.user.username)
    if(not actUser.is_superuser and actUser.username != username):
        return redirect(f'/cart/{request.user.username}/page')
    cart = Cart.objects.get(user__username=username)
    items = [cartitem for cartitem in cart.items.order_by('-product__name')]
    numProducts = 0
    fullPrice = 0
    for item in items:
        numProducts += item.quantity
        fullPrice += item.fullPrice
    if(cart.fullPrice != fullPrice or cart.products != numProducts):
        cart.fullPrice = fullPrice
        cart.products = numProducts
        cart.save()
    if(cart.checkoutCreation):
        diff = timezone.now() - cart.checkoutCreation
        if(cart.status == 'closed' and (diff.days > 0 or diff.seconds // 3600 >= 2)):
            cart.status = 'open'
            cart.save()
    cartUser = {'name': cart.user.name, 'username': cart.user.username}
    messages = Message.objects.filter(cart=cart).order_by("datetime")
    return render(request, 'cart/cart_page.html', {'cartUser': cartUser, 'cart': cart, 'items': items, 'user': actUser, 'messages': messages, 'debug':settings.DEBUG})


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


@login_required(login_url='/user/login')
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
        carts_items[cart.id] = cart.items.order_by("-datetime")
    return render(request, 'cart/cart_visualization.html', {'carts':carts, 'items':carts_items})


@login_required(login_url='/user/login')
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


@login_required(login_url='/user/login')
def confirm_purchase(request, username):
    user = CustomUser.objects.get(username=username)
    if(user.username == username):
        try:
            MelhorEnvioObject = MelhorEnvioAPI(user.is_superuser)
        except Exception as e:
            print(e.args[0])
            if("melhorenvio" in str(e)):
                instance = MelhorEnvioToken.objects.first()
                instance.prev_url = request.path
                instance.save()
                return redirect(e.args[0])
            else:
                return redirect(f'/cart/{request.user.username}/page')
        response = MelhorEnvioObject.calculate_shipping(user=user)
        for option in response:
            print(option)
            if 'error' in option.keys():
                response.remove(option)
        return render(request, 'cart/cart_confirm.html', {'freight': response})
    else:
        return redirect(f'/cart/{request.user.username}/page')


@login_required(login_url='/user/login')
def process_payment(request, username):
    body = json.loads(request.body)
    freightValue = float(body['freight_value'][2:])
    freightOption = body['freight_option']
    if request.method == "POST":
        cart = Cart.objects.get(user__username=username)
        cart.freightOption = freightOption
        cart.freightValue = freightValue
        response = PagSeguroAPI.generate_payment(cart)
        for item in response['links']:
            if item['rel'] == 'PAY':
                cart.paymentUrl = item['href']
                cart.checkoutCreation = timezone.now()
                cart.save()
                return JsonResponse(data={'payment_link':cart.paymentUrl}, status=200)
    return JsonResponse(data={}, status=500)


@login_required(login_url='/user/login')
def notification_handler(request):
    if request.method == "POST":
        notification_code = request.POST.get("notificationCode")
        notification_type = request.POST.get("notificationType")

        if notification_type == "transaction":
            transaction_details = PagSeguroAPI.get_transaction_details(notification_code)
            print(transaction_details)

    return HttpResponse(status=200)


@login_required(login_url="/user/login")
def thanks(request):
    user = request.user
    cart = user.cart
    cart.status = "paid"
    cart.paymentDatetime = timezone.now()
    cart.save()
    return render(request, 'cart/cart_thanks.html')


@login_required(login_url="/user/login")
@user_passes_test(lambda u: u.is_superuser)
def get_ticket(request, username):
    user = CustomUser.objects.get(username=username)
    MelhorEnvioObject = 0
    insertResponse = buyResponse = generateResponse = {'id':''}
    try:
        MelhorEnvioObject = MelhorEnvioAPI(user.is_superuser)
        insertResponse = MelhorEnvioObject.add_to_cart(user)
        print(insertResponse)
        buyResponse = MelhorEnvioObject.buy_shipments(insertResponse['id'])
        generateResponse = MelhorEnvioObject.generate_labels(insertResponse['id'])
    except Exception as e:
        print(e.args[0])
        if("melhorenvio" in str(e)):
            print(1)
            instance = MelhorEnvioToken.objects.first()
            instance.prev_url = request.path
            instance.save()
            return JsonResponse({"url":e.args[0]})
        else:
            print(2)
    #user.cart.status = "ticket"
    user.cart.shipmentId = insertResponse['id']
    user.cart.save()
    for item in user.cart.items.all():
        product = item.product
        product.numSold += item.quantity
        product.save()
    pdf_url = generateResponse.get('url')
    if not pdf_url:
        return HttpResponse("Link de impressão não encontrado", status=400)
    token_instance = MelhorEnvioToken.objects.first()
    generate_pdf = async_to_sync(generate_pdf_from_url)
    pdf = generate_pdf(pdf_url, token_instance.access_token)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Etiqueta {user.name}.pdf"'
    return response
