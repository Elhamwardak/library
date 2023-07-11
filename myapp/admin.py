from django.contrib import admin
from .models import Books, Profile, StudentBook, IssueBook,Category,Author,CustomUser
# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    list_display = ['title','author','issue_date']


    
admin.site.register(Books, BooksAdmin)
admin.site.register(Profile)
admin.site.register(StudentBook)
admin.site.register(IssueBook)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(CustomUser)




