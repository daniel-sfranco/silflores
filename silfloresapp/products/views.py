from django.shortcuts import render, redirect
from .models import Product, Photo, Tag
from django.contrib.auth.decorators import login_required, user_passes_test
from . import forms
from .product_handler import check_slug, tag_list

def products_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'products/products_list.html', {'products': products})

def product_page(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'products/product_page.html', {'product': product})

@login_required(login_url="/users/login/")
@user_passes_test(lambda u: u.is_superuser)
def product_new(request, product_id=None):
    if product_id:
        product = Product.objects.get(id=product_id)
        product_form = forms.ProductForm(instance=product)
    else:
        product = None
        product_form = forms.ProductForm()

    if request.method == "POST":
        product_form = forms.ProductForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        photo_uploaded = product_uploaded = False
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.slug = check_slug(product.name)
            tags = tag_list(product_form.cleaned_data['tags'])
            product.save()
            product.tags.set(tags)
            product_uploaded = True
            if photo_form.is_valid():
                photo_counter = 1
                for image in request.FILES.getlist('images'):
                    photo = Photo(product=product, photo=image, label=product.slug + '-' + str(photo_counter))
                    photo_counter += 1
                    photo.save()
                    photo_uploaded = True
        if product_uploaded and photo_uploaded:
            return redirect('products:list')
        else:
            photo_form = forms.PhotoForm
    else:
        product_form = forms.ProductForm()
        photo_form = forms.PhotoForm()
    return render(request, 'products/product_new.html', {"product_form":product_form, "photo_form":photo_form, "product":product})