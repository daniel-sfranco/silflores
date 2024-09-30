from .models import Product, Tag

def check_slug(name):
    split_name = name.lower().split()
    act_slug = '-'.join(split_name)
    for product in Product.objects.all():
        if product.slug == act_slug:
            act_slug += '-{}'.format(len(Product.objects.filter(slug__startswith=act_slug)))
            break
    return act_slug


def tag_list(tag_text: str):
    tags = [tag.strip() for tag in tag_text.split(',')]
    existing_tags = Tag.objects.filter(name__in=tags)
    new_tags = [Tag(name=tag) for tag in tags if tag not in existing_tags.values_list('name', flat=True)]
    Tag.objects.bulk_create(new_tags)
    all_tags = Tag.objects.filter(name__in=tags)
    return all_tags
