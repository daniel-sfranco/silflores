from django.contrib import admin
from .models import Cart, CartItem, Message, MelhorEnvioToken

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Message)
admin.site.register(MelhorEnvioToken)