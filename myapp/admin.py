from django.contrib import admin
from .models import Books, Profile, StudentBook, IssueBook,Category,Author,CustomUser
from.forms import UserForm
from django.utils.html import format_html
# Register your models here.

class UserFormm(admin.ModelAdmin):
    radio_fields = {'gender': admin.HORIZONTAL}
    form = UserForm

class BooksAdmin(admin.ModelAdmin):
    list_display = ['title','author','issue_date']
    
admin.site.register(Books, BooksAdmin)
admin.site.register(Profile)
admin.site.register(StudentBook)
admin.site.register(IssueBook)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(CustomUser)




