from django.forms import ModelForm, widgets
from .models import Books
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class BookForm(ModelForm):

    class Meta:
        model = Books
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'cover_photo':forms.FileInput(attrs={'class':'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control'}),
            'book_file':forms.FileInput(attrs={'class':'form-control'})
        }



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder' : 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder' : 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder' : 'Password Confirmation'}),
        }
