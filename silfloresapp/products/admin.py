from django.contrib import admin
from .models import Product, Tag, Photo

# Register your models here.
admin.site.register(Product)
admin.site.register(Photo)
admin.site.register(Tag)
