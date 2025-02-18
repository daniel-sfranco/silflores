from django import forms
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class UserPhotoWidget(forms.ClearableFileInput):
    template_name = 'users/user_photo_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['is_initial'] = self.is_initial(value)
        return context


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'cpf', 'email', 'ddd', 'phone', 'birthday', 'cep', 'home_number', 'complement', 'photo', 'username']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['photo', 'name', 'username', 'cpf', 'email', 'ddd', 'phone', 'birthday', 'cep', 'home_number', 'complement']
        widgets = {
            'photo': UserPhotoWidget(),
        }


    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            for field_name in self.fields:
                self.fields[field_name].initial = getattr(instance, field_name)
        self.fields.pop('password')
