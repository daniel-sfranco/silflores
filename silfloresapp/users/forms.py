from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'cpf', 'email', 'phone', 'birthday', 'cep', 'home_number', 'complement', 'username']