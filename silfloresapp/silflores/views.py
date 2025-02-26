from django.shortcuts import render
from products.models import Product, Photo, Tag

def home(request):
    soldProducts = Product.objects.all().order_by('-numSold')[:20]
    return render(request, 'home.html', {'soldProducts': soldProducts})

def about(request):
    return render(request, 'about.html')

def meme(request):
    return render(request, 'meme.html')
