from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    size_types = {
        'fixed': 'Tamanho único',
        'choice': 'Selecionar tamanho',
        'set': 'Definir valor'
    }
    name = models.CharField(max_length=150, verbose_name="Nome do Produto")
    price = models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name="Preço")
    desc = models.TextField(default='', verbose_name="Descrição")
    size_type = models.CharField(choices=size_types, default='', verbose_name='Tipo de tamanho')
    size = models.CharField(default='', verbose_name='Tamanho (cm)')
    term = models.IntegerField(blank=True, verbose_name='Prazo de produção')
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(blank=True)

    def __str__(self) -> str:
        return str(self.name)


class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos', default=None)
    photo = models.FileField(upload_to="products/")
    label = models.CharField(max_length=155, blank=True)

    def __str__(self):
        return self.label
