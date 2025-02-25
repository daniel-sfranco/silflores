from django import forms
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from cloudinary.forms import CloudinaryFileField
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'cpf', 'email', 'ddd', 'phone', 'birthday', 'cep', 'home_number', 'complement', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'cpf', 'email', 'ddd', 'phone', 'birthday', 'cep', 'home_number', 'complement']


    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            for field_name in self.fields:
                self.fields[field_name].initial = getattr(instance, field_name)
        self.fields.pop('password')
