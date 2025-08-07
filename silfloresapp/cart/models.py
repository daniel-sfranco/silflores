from django.db import models
from users.models import CustomUser
from products.models import Product


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    fullPrice = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    products = models.IntegerField(default=0)
    status = models.CharField(default="open")
    freightOption = models.IntegerField(default=0)
    freightValue = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    paymentUrl = models.CharField(default='')
    labelUrl = models.CharField(default='', null=True)
    trackingUrl = models.CharField(default='', null=True)
    checkoutCreation = models.DateTimeField(null=True)
    paymentDatetime = models.DateTimeField(null=True)
    shipmentId = models.CharField(null=True)

    def __str__(self):
        return f"{self.user.username}'s cart"


class CartItem(models.Model):
    itemName = models.SlugField(blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    fullPrice = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return f"{self.cart.user.username}'s {self.product.name}"


class Message(models.Model):
    content = models.TextField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.datetime.day}/{self.datetime.month}/{self.datetime.year % 100} {self.datetime.hour}:{self.datetime.minute} - {self.sender.username}: {self.content}"


class Coupon(models.Model):
    types = {
        'fixed': 'fixo',
        'variable': 'porcentagem',
    }
    name = models.CharField(max_length=20, verbose_name="Nome")
    type = models.CharField(choices=types, verbose_name="Tipo")
    value = models.DecimalField(decimal_places=2, max_digits=6)


class MelhorEnvioToken(models.Model):
    access_token = models.TextField(blank=True)
    expires_in = models.DateTimeField()
    prev_url = models.CharField(max_length=255, blank=True)
    sandbox = models.BooleanField(default=False)
