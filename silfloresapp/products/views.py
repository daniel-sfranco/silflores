from django.shortcuts import render
from .models import Product
from django.contrib.auth.decorators import login_required, user_passes_test

def products_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'products/products_list.html', {'products': products})

def product_page(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'products/product_page.html', {'product': product})

@login_required(login_url="/users/login/")
@user_passes_test(lambda u: u.is_superuser)
def product_new(request):
    return render(request, 'products/product_new.html')