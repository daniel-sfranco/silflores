from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.name)


class Photo(models.Model):
    photo = models.ImageField()
    label = models.CharField(max_length=50, default='')

    def __str__(self) -> str:
        return str(self.label)


class Product(models.Model):
    size_types = {
        'fixed': 'Tamanho fixo',
        'choice': 'Selecionar tamanho',
        'set': 'Definir valor'
    }
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    tags = models.ManyToManyField(Tag)
    desc = models.TextField(default='')
    size_type = models.CharField(choices=size_types, default='')
    size = models.CharField(default='')
    term = models.IntegerField(null=True)
    photos = models.ManyToManyField(Photo)

    def __str__(self) -> str:
        return str(self.name)
