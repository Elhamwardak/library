from django.forms import ModelForm, widgets
from .models import Books, IssueBook,Category, CustomUser,ContactUs
from django.core.validators import RegexValidator
from django import forms


# Every letters to LowerCase
# class Lowercase(forms.CharField):
#     def to_python(self, value):
#         return value.lower()

# Every letters to UpperCase
# class Uppercase(forms.CharField):
#     def to_python(self, value):
#         return value.upper()

class BookForm(ModelForm):

    # VALIDATIONS
    isbn_number = forms.CharField(
        label = 'ISBN',min_length = 0, max_length = 10,
        validators=[RegexValidator(r'^[0-9]+$',message="only number is allowed!")],
        widget = forms.TextInput(attrs={'placeholder':'isbn number'})
    )
    title = forms.CharField(
        label = 'Title',min_length = 4, max_length = 20,
        validators=[RegexValidator(message="put the book title here!")],
        widget = forms.TextInput(attrs={'placeholder':'book title'})
    )
    available_quantity = forms.CharField(
        label = 'Available Quantity',min_length = 0, max_length = 100,
        required=False,
        validators=[RegexValidator(message="Only number is allowed!")],
        widget = forms.TextInput(attrs={'type':'number'})
    )
    book_descriptions = forms.CharField(
        label = 'Descriptions',min_length = 0, max_length = 1000,        
        required=False,
        validators=[RegexValidator(message="descriptions about book!")],
        widget = forms.Textarea(attrs={'placeholder':'Put some informations about book','rows':5})
    )

    class Meta:
        model = Books
        fields = '__all__'

        # widgets = {
        #     'isbn_number':forms.TextInput(attrs={'class':'form-control'}),
        #     'title': forms.TextInput(attrs={'class': 'form-control'}),
        #     'book_descriptions': forms.TextInput(attrs={'class': 'form-control'}),
        #     'category': forms.Select(attrs={'class': 'form-select'}),
        #     'available_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'cover_photo':forms.FileInput(attrs={'class':'form-control'}),
        #     'author': forms.Select(attrs={'class': 'form-select'}),
        #     'issue_date': forms.DateInput(attrs={'class': 'form-control'}),
        #     'book_file':forms.FileInput(attrs={'class':'form-control'})
        # }
        # labels = {
        #     'title':'Book Title',
        #     'isbn_number':'ISBN',
        #     'file':'Choose File'
        # }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =  ['name','status']


        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields =  ['name']

#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'})   
#         }

class UserForm(forms.ModelForm):


    # VALIDATIONS
    username = forms.CharField(
        label = 'Username',min_length = 4, max_length = 30,
        validators=[RegexValidator(r'^(?=.*[a-zA-Z])(?=.*\d).+$',message="charecters + number is allowed!")]
    )
    email = forms.CharField(
        label = 'Email address',min_length = 4, max_length = 30,
        validators=[RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',message="please enter the correct email address!")]
    )
    GENDER_CHOICES = [('M','Male'),('F','Female')]
    gender = forms.CharField(label='Gender',widget=forms.RadioSelect(choices=GENDER_CHOICES))
    
    password = forms.CharField(
        label = 'Password',min_length = 4, max_length = 30,
        validators=[RegexValidator(r'^(?=.*[a-zA-Z])(?=.*\d).+$',message="please enter the correct password!")],
        widget = forms.PasswordInput(attrs={'type':'password'})
    )
    class Meta:
        model=CustomUser
        fields=['username', 'first_name','father_name', 'last_name', 'gender', 'phone_number', 'user_id', 'password', 'email', 'group']

        widgets = {
            'phone_number': forms.TextInput(attrs={'data-mask':'(00)00-000-0000'}),
            # 'gender':forms.TextInput(attrs={'class':'form-check',type':'radio'}),
            'user_id': forms.TextInput(attrs={'placeholer':'Example= BCS-98-968'}),
            # 'gender':forms.RadioSelect(attrs={'type':'radio'})
        }

class ContactForm(forms.ModelForm):

    message = forms.CharField(
        label='Message',
        widget = forms.Textarea(attrs={'placeholder':'Write your message','rows':7})
    )
    class Meta:
        model = ContactUs
        fields = '__all__'
