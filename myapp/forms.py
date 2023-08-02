from django.forms import ModelForm, widgets
from .models import Books, IssueBook,Category,Author, CustomUser
from django.core import validators
from django import forms


class BookForm(ModelForm):

    class Meta:
        model = Books
        fields = '__all__'

        widgets = {
            'isbn_number':forms.TextInput(attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'cover_photo':forms.FileInput(attrs={'class':'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control'}),
            'file':forms.FileInput(attrs={'class':'form-control'})
        }

        labels = {
            'title':'Book Title',
            'isbn_number':'ISBN',
            'file':'Choose File'
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

class UserForm(forms.ModelForm):

    class Meta:
        model=CustomUser
        fields=['username', 'first_name','father_name', 'last_name', 'gender', 'phone_number', 'user_id', 'password', 'email', 'group']
