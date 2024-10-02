from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'cpf', 'email', 'phone', 'birthday', 'cep', 'home_number', 'complement', 'photo', 'username']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['photo', 'name', 'username', 'cpf', 'email', 'phone', 'birthday', 'cep', 'home_number', 'complement']

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            for field_name in self.fields:
                self.fields[field_name].initial = getattr(instance, field_name)
        self.fields.pop('password')
