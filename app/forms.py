from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'tags': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title


# forms.py
class RegisterUserForm(UserCreationForm):
    login = forms.CharField(label='Login', max_length=30, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label='NickName', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    photo = forms.ImageField(required=False, label='Avatar', widget=forms.ClearableFileInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('login', 'email', 'username', 'password1', 'password2', 'photo')


class LoginUserForm(AuthenticationForm):
    login = forms.CharField(label='Login', max_length=30, widget=forms.TextInput(attrs={'class': 'form-input'}))

    def clean(self):
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')

        if login and password:
            # можно выполнить здесь дополнительные проверки логина, если это необходимо
            pass

        return super().clean()

