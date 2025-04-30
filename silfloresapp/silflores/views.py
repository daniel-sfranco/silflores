import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.conf import settings
from products.models import Product
from cart.melhorenvio_service import MelhorEnvioAPI
from cart.models import MelhorEnvioToken

def home(request):
    code = request.GET.get('code')
    if(code):
        melhorEnvioToken = MelhorEnvioToken.objects.get(sandbox=settings.MELHOR_ENVIO_SANDBOX)
        melhorEnvioObject = MelhorEnvioAPI(request.user.is_superuser, check=False)
        melhorEnvioObject.refresh_melhorenvio_token(code=code)
        return redirect(melhorEnvioToken.prev_url)
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def meme(request):
    return render(request, 'meme.html')

def getSoldProducts(request):
    totalProductQuantity = Product.objects.all().count()
    numSoldProducts = min(totalProductQuantity, 20)
    soldProductsQuery = Product.objects.all().order_by('-numSold')[:numSoldProducts]
    soldProducts = [{'name': product.name, 'desc': product.desc, 'imageUrl': product.firstPhoto.url} for product in soldProductsQuery]
    return JsonResponse({'soldProducts': json.dumps(soldProducts), 'numSoldProducts': numSoldProducts})

def getNewProducts(request):
    totalProductQuantity = Product.objects.all().count()
    numNewProducts = min(totalProductQuantity, 20)
    newProductsQuery = Product.objects.all().order_by('-createdAt')[:numNewProducts]
    newProducts = [{'name': product.name, 'desc': product.desc, 'imageUrl': product.firstPhoto.url} for product in newProductsQuery]
    return JsonResponse({'newProducts': json.dumps(newProducts), 'numNewProducts': numNewProducts})
