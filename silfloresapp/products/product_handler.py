from .models import Product

def check_slug(name):
    split_name = name.lower().split()
    act_slug = '-'.join(split_name)
    for product in Product.objects.all():
        if product.slug == act_slug:
            act_slug += '-{}'.format(len(Product.objects.filter(slug__startswith=act_slug)))
            break
    return act_slug