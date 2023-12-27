from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *
from django import forms



class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким адресом электронной почты уже существует")
        return email
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    STATUS_CHOICES = (
        ('teacher', 'Учитель'),
        ('student', 'Ученик'),
    )

    full_name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-input'}))
    status = forms.ChoiceField(label='Статус', choices=STATUS_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'full_name', 'status')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
