
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import pre_save, post_save 
from django.db import models
from .manager import CutomUserManager
from django.utils import timezone



# GENDER_CHOICES = (
#     ('M', 'Male'),
#     ('F', 'Female')
# )
class CustomUser(AbstractUser):

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    user_id = models.CharField(max_length=50,null=True,blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=2)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CutomUserManager()

    

# class Author(models.Model):
#     name = models.CharField(max_length=100,null=True, blank=True)

#     def __str__(self):
#         return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    @property
    def status_name(self):
        return "Active" if self.status else "Inactive"
    
    def __str__(self):
        return self.name
    
class Books(models.Model):
    isbn_number = models.CharField(max_length=20,null=True,blank=True)
    title = models.CharField(max_length=20)
    book_descriptions = models.TextField(max_length=1000, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    available_quantity = models.IntegerField(default=0)
    cover_photo = models.ImageField(
        upload_to='images/', null=True, blank=True,  default='images/default.jpg')
    issue_date = models.DateField(auto_now_add=True)
    book_file = models.FileField(upload_to="files/",null=True,blank=True)
    author = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['issue_date']


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)


class StudentBook (models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False, blank=False, null=False)
    is_favourite = models.BooleanField(default=False, blank=False, null=False)

class IssueBook(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    returned_date = models.DateField(default=None, null=True, blank=True)
    quantity_issued = models.IntegerField(default=1)

class ContactUs(models.Model):
    full_name = models.CharField(max_length=30)
    phone_number = models.IntegerField()
    email = models.EmailField(max_length=50)
    message = models.TextField()
    is_read = models.BooleanField(default=False, null=True)

    class meta:
        ordering = ['is_read']


class Student(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='student_user', null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    gender = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    


class Teacher(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='teacher_user', null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    gender = models.CharField(max_length=50, null=True, blank=True)