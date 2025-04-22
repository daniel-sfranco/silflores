import json
from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product, Photo, Tag

def home(request):
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
