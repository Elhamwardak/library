from django.contrib import admin
from .models import Books, Profile, StudentBook
# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    list_display = ['title','author','issue_date']


    
admin.site.register(Books, BooksAdmin)
admin.site.register(Profile)
admin.site.register(StudentBook)

