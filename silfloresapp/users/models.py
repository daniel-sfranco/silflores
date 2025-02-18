from django.db import models #type:ignore
from django.contrib.auth.models import AbstractUser #type:ignore
from cloudinary.models import CloudinaryField

# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=200, verbose_name="Nome Completo", blank=True)
    #photo = models.ImageField(blank=True, verbose_name="Foto de perfil (opcional)", null=True)
    photo = CloudinaryField('imagem')
    cpf = models.CharField(verbose_name="CPF (só números)", unique=True, blank=True)
    email = models.EmailField(verbose_name="Email", unique=True)
    phone = models.CharField(max_length=10, verbose_name="Telefone (só números)", blank=True)
    ddd = models.IntegerField(blank=True, default=11, verbose_name="DDD")
    birthday = models.CharField(verbose_name="Data de Nascimento", blank=True)
    cep = models.CharField(max_length=9, verbose_name="CEP", blank=True)
    home_number = models.IntegerField(verbose_name="Número", default=0)
    complement = models.CharField(max_length=10, verbose_name="Complemento", blank=True)

    def __str__(self):
        return self.username
