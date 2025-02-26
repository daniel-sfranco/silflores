import json
from django.shortcuts import render, redirect
from django.db.models import IntegerField, Count, Case, When
from django.db.models.functions import Lower
from django.utils import timezone
from .models import Product, Photo, Tag
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from . import forms
from .product_handler import check_slug, tag_list, count_matching_words
from cart.models import CartItem
from math import trunc


def product_collections(request):
    tags = Tag.objects.order_by('-lastChanged')
    if tags.count() > 1:
        return render(request, 'products/product_collections.html', {'tags': tags, 'empty': False})
    else:
        return render(request, 'products/product_collections.html', {'tags': tags, 'empty': True})


def products_list(request, tagName, searchTerm=None):
    tags = []
    lowerPrice = 0
    upperPrice = 10000
    if(searchTerm):
        searchWords = searchTerm.strip().lower().split()
    else:
        searchWords = False

    if(request.method == "POST"):
        data = json.loads(request.body)
        products = Product.objects.all()
        if data['selectedTags']:
            tags = [tag for tag in Tag.objects.filter(name__in=data['selectedTags'])]
            products = products.filter(tags__in=tags)
        if 'lowerPrice' in data.keys():
            lowerPrice = int(data['lowerPrice'])
            products = products.filter(price__gte=lowerPrice)
        if 'upperPrice' in data.keys():
            upperPrice = int(data['upperPrice'])
            products = products.filter(price__lte=upperPrice)
        if data['stockAvaliable']:
            products = products.exclude(stock=0)
        if(searchWords):
            products = sorted(products, key=lambda product: count_matching_words(searchWords, product.slug))
            for product in products:
                if(count_matching_words(searchWords, product.slug) == 0):
                    products.remove(product)
        product_list = []
        for product in products:
            json_formatted = {'name': product.name, 'price': product.price, 'slug': product.slug}
            if json_formatted not in product_list:
                product_list.append(json_formatted)
        return JsonResponse({"products": product_list})
    else:
        tags = [Tag.objects.get(name=tagName)]
        products = Product.objects.filter(tags__in=tags).filter(price__lte=upperPrice).filter(price__gte=lowerPrice)
        if(searchWords):
            products = sorted(products, key=lambda product: count_matching_words(searchWords, product.slug))
            for product in products:
                if(count_matching_words(searchWords, product.slug) == 0):
                    products.remove(product)
        return render(request, 'products/products_list.html', {'products': products, 'all': Tag.objects.get(name='all'), 'tags': Tag.objects.exclude(name='all').order_by('name'), 'actual': tagName})


def product_page(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'products/product_page.html', {'product': product})


@login_required(login_url="/user/login/")
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
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.slug = check_slug(product.name)
            tags = tag_list(product_form.cleaned_data['tags'] + ', all')
            product.numPhotos = len(request.FILES.getlist('images'))
            product.firstPhoto = request.FILES.getlist('images')[0]
            product.save()
            if photo_form.is_valid():
                i = 1
                for image in request.FILES.getlist('images'):
                    photo = Photo(product=product, photo=image, label=product.slug + '-' + str(i))
                    i += 1
                    photo.save()
            product.tags.set(tags)
            for tag in product.tags.all():
                tag.lastChanged = timezone.now()
                tag.numProducts += 1
                tag.save()
            return redirect('products:collections')
        else:
            photo_form = forms.PhotoForm
    else:
        product_form = forms.ProductForm()
        photo_form = forms.PhotoForm()
    return render(request, 'products/product_new.html', {"product_form":product_form, "photo_form":photo_form, "product":product})


@login_required(login_url="/user/login")
@user_passes_test(lambda u:u.is_superuser)
def product_delete(request, slug):
    product = Product.objects.get(slug=slug)
    tags = product.tags.all()
    for tag in tags:
        tag.lastChanged = timezone.now()
        tag.numProducts -= 1
        tag.save()
    product.delete()
    return redirect('/products/')


@login_required(login_url='/user/login')
@user_passes_test(lambda u: u.is_superuser)
def product_update(request, slug):
    product = Product.objects.get(slug=slug)
    product_size = product.size
    if request.POST:
        product_form = forms.ProductChangeForm(request.POST, instance=product)
        photo_form = forms.PhotoForm(request.POST, request.FILES, required=False);
        if product_form.is_valid():
            product = product_form.save(commit=False)
            if photo_form.is_valid():
                photo_counter = 1
                for image in request.FILES.getlist('images'):
                    while(Photo.objects.filter(label=product.slug + '-' + str(photo_counter)).exists()):
                        photo_counter += 1
                    photo = Photo(product=product, photo=image, label=product.slug + '-' + str(photo_counter))
                    photo_counter += 1
                    photo.save()
            product.numPhotos = photo_counter
            if(product.size != product_size):
                CartItem.objects.filter(cart=request.user.cart).filter(product=product).delete()
                if(product.size == 'choice'):
                    sizeOptions = [float(s.strip()) for s in product.size.split(",")]
                    i = 0
                    for size in sizeOptions:
                        actObject = CartItem(cart=request.user.cart, product=product, quantity=0, fullPrice=product.price)
                        actObject.save()
                elif(product.size == 'fixed'):
                    sizeObject = CartItem(cart=request.user.cart, product=product, quantity=0, fullPrice=product.price, size=float(product.size))
                    sizeObject.save()
            product.save()
            tags = tag_list(product_form.cleaned_data['tags'])
            product.tags.set(tags)
            return redirect(f'/products/{slug}')
    else:
        product_form = forms.ProductChangeForm(instance=product)
        photo_form = forms.PhotoForm(required=False)
    return render(request, 'products/product_update.html', {'product': product, 'product_form': product_form, 'photo_form': photo_form})


@login_required(login_url='/user/login')
@user_passes_test(lambda u: u.is_superuser)
def photo_delete(request, pk):
    photo = Photo.objects.get(id=pk)
    product = photo.product
    photo.delete()
    product.numPhotos -= 1
    product.save()
    return redirect(f'/products/{product.slug}/update')
