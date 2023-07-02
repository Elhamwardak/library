from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save 


class Category(models.Model):
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    @property
    def status_name(self):
        return "Active" if self.status else "Inactive"
    
    def __str__(self):
        return self.name
    
class Books(models.Model):
    title = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.CharField(max_length=20, null=True, blank=True)
    available_quantity = models.IntegerField(default=0)
    cover_photo = models.ImageField(
        upload_to='images/', null=True, blank=True,  default='images/default.jpg')
    issue_date = models.DateField(auto_now_add=True)

  

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

class IssueBook(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    returned_date = models.DateField(default=None, null=True, blank=True)
    quantity_issued = models.IntegerField(default=1)

