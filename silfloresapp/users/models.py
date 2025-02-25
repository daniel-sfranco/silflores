from django.core.files.uploadedfile import UploadedFile
from django.db import models #type:ignore
from django.contrib.auth.models import AbstractUser #type:ignore
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError

FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 10  # 10mb

def file_validation(file):
    if not file:
        raise ValidationError("No file selected.")
    if isinstance(file, UploadedFile):
        if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError("File shouldn't be larger than 10MB.")

class CustomUser(AbstractUser):
    name = models.CharField(max_length=200, verbose_name="Nome Completo", blank=True)
    cpf = models.CharField(verbose_name="CPF (só números)", unique=True, blank=True)
    email = models.EmailField(verbose_name="Email", unique=True)
    phone = models.CharField(max_length=9, verbose_name="Telefone (só números)", blank=True)
    ddd = models.IntegerField(blank=True, default=11, verbose_name="DDD")
    birthday = models.CharField(verbose_name="Data de Nascimento", blank=True)
    cep = models.CharField(max_length=9, verbose_name="CEP", blank=True)
    home_number = models.IntegerField(verbose_name="Número", default=0)
    complement = models.CharField(max_length=10, verbose_name="Complemento", blank=True)

    def __str__(self):
        return self.username
