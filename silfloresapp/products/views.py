from django.shortcuts import render
from .models import Product
from django.http import HttpResponse

def products_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'products/products_list.html', {'products': products})

def product_page(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'products/product_page.html', {'product': product})