from django.forms import ModelForm, widgets
from .models import Books, IssueBook,Category,Author
from django.core import validators
from django import forms
# from django.contrib.auth import get_user_model

# user = get_user_model()


class BookForm(ModelForm):

    class Meta:
        model = Books
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'cover_photo':forms.FileInput(attrs={'class':'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =  ['name','status']


        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields =  ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})   
        }
