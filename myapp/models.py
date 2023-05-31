from django.contrib.auth.models import User
from django.db import models
# from django.contrib.auth.models import AbstractUser
# from .manager import UserManager

from django.db.models.signals import pre_save, post_save 


class Books(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=100)
    price = models.IntegerField(default=0, null=True, blank=True)
    author = models.CharField(max_length=20, null=True, blank=True)
    cover_photo = models.ImageField(
        upload_to='images/', null=True, blank=True, default="default.jpg")
    issue_date = models.DateTimeField(auto_now_add=True)
    book_file = models.FileField(
        upload_to='files/', null=False, default="")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['issue_date']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)


class StudentBook (models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False, blank=False, null=False)
    is_favourite = models.BooleanField(default=False, blank=False, null=False)

# class User(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True)
#     first_name = models.TextField(max_length=150)
#     last_name = models.TextField(max_length=150)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'

#     REQUIRED_FIELDS = []
    