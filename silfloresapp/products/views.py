from django.shortcuts import render, redirect
from .models import Product, Photo, Tag
from django.contrib.auth.decorators import login_required, user_passes_test
from . import forms
from .product_handler import check_slug, tag_list
from users.models import CustomUser


def products_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'products/products_list.html', {'products': products})


def product_page(request, slug):
    product = Product.objects.get(slug=slug)
    user = CustomUser.objects.get(username=request.user.username)
    return render(request, 'products/product_page.html', {'product': product, 'user': user})


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
            tags = tag_list(product_form.cleaned_data['tags'])
            if photo_form.is_valid():
                product.numPhotos = 1
                for image in request.FILES.getlist('images'):
                    photo = Photo(product=product, photo=image, label=product.slug + '-' + str(product.numPhotos))
                    product.numPhotos += 1
                    photo.save()
            product.save()
            product.tags.set(tags)
            return redirect('products:list')
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
    product.delete()
    return redirect('/products/')


@login_required(login_url='/user/login')
@user_passes_test(lambda u: u.is_superuser)
def product_update(request, slug):
    product = Product.objects.get(slug=slug)
    if request.POST:
        product_form = forms.ProductChangeForm(request.POST, instance=product)
        photo_form = forms.PhotoForm(request.POST, request.FILES);
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
            product.save()
            tags = tag_list(product_form.cleaned_data['tags'])
            product.tags.set(tags)
            return redirect(f'/products/{slug}')
    else:
        product_form = forms.ProductChangeForm(instance=product)
        photo_form = forms.PhotoForm
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
