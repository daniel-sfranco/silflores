from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=200, verbose_name="Nome Completo", blank=True)
    photo = models.ImageField(blank=True, verbose_name="Foto de perfil (opcional)", default="fallback_user.png")
    cpf = models.CharField(verbose_name="CPF (só números)", unique=True, blank=True)
    email = models.EmailField(verbose_name="Email", unique=True)
    phone = models.CharField(max_length=15, verbose_name="Telefone (só números)", blank=True)
    birthday = models.CharField(verbose_name="Data de Nascimento", blank=True)
    cep = models.CharField(max_length=10, verbose_name="CEP", blank=True)
    home_number = models.IntegerField(verbose_name="Número", default=0)
    complement = models.CharField(max_length=10, verbose_name="Complemento", blank=True)

    def __str__(self):
        return self.username
