from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    size_types = {
        'fixed': 'Tamanho fixo',
        'choice': 'Selecionar tamanho',
        'set': 'Definir valor'
    }
    # Tirar os valores que podem ser nulos daqui
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    tags = models.ManyToManyField(Tag)
    desc = models.TextField(default='')
    size_type = models.CharField(choices=size_types, default='')
    size = models.CharField(default='')
    term = models.IntegerField(blank=True) # prazo de produção
    slug = models.SlugField(blank=True)

    def __str__(self) -> str:
        return str(self.name)


class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos', default=None)
    photo = models.FileField(upload_to="products/")

    def __str__(self) -> str:
        return str(self.label)
