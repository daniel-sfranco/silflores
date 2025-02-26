from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)
    lastChanged = models.DateTimeField(auto_now_add=True)
    numProducts = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    sizes = {
        'fixed': 'Tamanho único',
        'set': 'Definir valor'
    }
    name = models.CharField(max_length=150, verbose_name="Nome do Produto")
    price = models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name="Preço")
    desc = models.TextField(default='', verbose_name="Descrição")
    size = models.CharField(choices=sizes, default='', verbose_name='Tipo de tamanho')
    term = models.IntegerField(blank=True, verbose_name='Prazo de produção')
    stock = models.IntegerField(default=0, verbose_name='Estoque (0 para encomenda)')
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(blank=True)
    numPhotos = models.IntegerField(default=0)
    numSold = models.IntegerField(default=0)
    firstPhoto = CloudinaryField('imagem', null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)


class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos', default=None)
    photo = CloudinaryField('imagem')
    label = models.CharField(max_length=155, blank=True)

    def __str__(self):
        return self.label
