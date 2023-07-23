from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import *
from .forms import BookForm,CategoryForm,AuthorForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenicated_user, allowed_users, admin_only
from .utils import searchbooks, paginateBooks,searchuser,paginateUsers
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta,date
from .signals import *
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError


User = get_user_model() 
# Create your views here.

@login_required(login_url='login-page')
@admin_only
def Admin(request):
    today = timezone.now().date()
    total_issued_books_today = IssueBook.objects.filter(issue_date=today).count()

    total_issued = IssueBook.objects.count()

    total_books = Books.objects.count()

    total_users = User.objects.count()

    total_authors = Author.objects.count()

    total_categories = Category.objects.count()

    today = timezone.now().date()
    five_days_later = today + timedelta(days=7)
    deadline_returns_book = IssueBook.objects.filter(expected_return_date__lte= five_days_later,
                                                      expected_return_date__gt=today,
                                                      returned_date=None
                                                      )
    count_books_not_returned = deadline_returns_book.count()

    context = {'totalbooks':total_books,'totalusers':total_users,'total_issued':total_issued,
               'total_issued_books_today':total_issued_books_today,'count_books_not_returned':count_books_not_returned,
               'total_authors':total_authors,'total_categories':total_categories}
    return render(request, 'home.html',context)

# Books Management
@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def book_list(request):
    books, search_book = searchbooks(request)
    custom_range,  books = paginateBooks(request, books, 5)

    context = {'books': books,'search_book':search_book,'custom_range':custom_range}
    return render(request, 'book_list.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def add_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        form.save()
        messages.success(request,"Book Successfully added")
        return redirect('books-management')

    context = {'form': form}
    return render(request, 'add_book.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def Update_book(request, id):
    if request.method == 'POST':
        book = Books.objects.get(pk=id)
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()

        messages.success(request,'Successfully Updated!')
        return redirect('books-management')
    else:
        book = Books.objects.get(pk=id)
        form = BookForm(instance=book)

    context = {'form': form}
    return render(request, 'update_book.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def Delete_book(request, id):
    book = Books.objects.get(pk=id)
    book.delete()
    messages.success(request,'Book Deleted!')
    return redirect('books-management')

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def booksnotreturnyet(request):
    today = timezone.now().date()
    five_days_later = today + timedelta(days=7)
    deadline_returns_book = IssueBook.objects.filter(expected_return_date__lte= five_days_later,
                                                      expected_return_date__gt=today,
                                                      returned_date=None
                                                      )

    context={'deadline_returns_book':deadline_returns_book}
    return render(request,'books_not_return.html',context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def issue_book(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        expected_return_date = request.POST.get('expected_return_date')
        
        user = User.objects.exclude(is_superuser=True).get(pk=user_id)
        book = Books.objects.get(pk=book_id)

        book.available_quantity = book.available_quantity - 1
        book.save()

        IssueBook.objects.create(
            user_id=user,
            book_id=book,
            expected_return_date=expected_return_date
        )
        messages.success(request, 'Book issue created successfully.')
        return redirect('view-issuebook',books='all')
    else:
        users = User.objects.exclude(is_superuser=True).all()
        books = Books.objects.filter(available_quantity__gt= 0)

        context = {'users':users, 'books':books}
        return render(request, 'issue_book.html', context)
    
@allowed_users(allowed_roles=['admin'])    
@login_required(login_url='login-page')
def ViewIssueBook(request,books):
    if books == "all":
        issuebook = IssueBook.objects.all()
        context = {'issuebook': issuebook,'title':'Issued Books'}
    else:
        today = timezone.now().date()
        total_issued_books_today = IssueBook.objects.filter(issue_date=today)
        context = {'total_issued_books_today': total_issued_books_today, 'title': 'Today\'s Issued Books'} 
 
    return render(request, 'view_issuebook.html', context)
# CRUD system for Category section
def categorylist(request):
    category = Category.objects.all()
    context={'category':category}
    return render(request,'category_list.html',context)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

def update_category(request, id):
    category = Category.objects.get(pk=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request,'update_category.html',{'form':form})

def delete_category(request, id):
    category = Category.objects.get(pk=id)
    category.delete()
    return redirect('category-list')

# CRUD system for Authors section

def authorslist(request):
    author = Author.objects.all()
    context={'author':author}
    return render(request,'author_list.html',context)

def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author-list')
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})

def update_author(request, id):
    author = Author.objects.get(pk=id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author-list')
    else:
        form = AuthorForm(instance=author)
    return render(request,'update_author.html',{'form':form})

def delete_author(request, id):
    author = Author.objects.get(pk=id)
    author.delete()
    return redirect('author-list')

# Users Managements
@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def user_list(request):

    users, search_user = searchuser(request)
    custom_range,  users = paginateUsers(request, users, 6)

    context = {'users': users,'search_user':search_user,'custom_range':custom_range}
    return render(request, 'users_list.html', context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = CustomUser.objects.create(**data)
            user.set_password(data['password'])
            user.save()
            messages.success(request,"User successfully added")
            return redirect('users-management')
    groups = Group.objects.filter(~Q(name='admin'))
    return render(request, 'add_user.html', {'groups': groups})


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def Update_user(request, id):
    if request.method == 'POST':
        user = User.objects.get(pk=id)
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.father_name = request.POST['father_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.phone_number = request.POST['phone_number']
        user.user_id = request.POST['user_id']
        user.gender = request.POST['gender']
        user = user.save()

        messages.success(request,'You have Successfully updated the user')
        return redirect('users-management')

    else:
       pass


    user = User.objects.get(pk=id)
    return render(request, 'update_user.html', {'user': user} )


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def Delete_user(request, id):
    users = CustomUser.objects.get(pk=id)
    users.delete()
    messages.success(request, 'Deleted User')
    return redirect('users-management')


#login , logout
def Index(request):
    return render(request, 'login-page.html')


@unauthenicated_user
def LoginPage(request):
 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin-page')
        else:
            messages.error(request, 'Email or Password is incorrect!')

    context = {}
    return render(request, 'index.html', context)


@unauthenicated_user
def registerPage(request):
    if request.method == 'POST':
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            user_id = request.POST['user_id']
            group= request.POST['group']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email,phone_number=phone_number,user_id=user_id,
                                                group=group,password1=password1,password2=password2)
            user.save()
        return redirect('users-management')

    return render(request, 'register_page.html')
   

def logoutUser(request):
    logout(request)
    return redirect('login-page')

def user_profile(request):
    # if request.user.is_authenticated:
    #     if request.method == 'POST':
    #         user = request.user
    #         form = CustomUser(request.POST, instance=user)
    #         if form.is_valid():
    #             form.save()
    #             login(request, user)
    #         return redirect('user-profile')
    #     else:
    #         user = request.user
    #         form = CustomUser(instance=user)

        # context = {'form': form, 'user_group' : user.groups.get}
    return render(request, 'user_profile.html')
    # else:
    #     return redirect('login-page')

# Books Pages for students
def issuebook_to_student(request):
    issuebook = IssueBook.objects.filter(user_id=request.user.id)
    issuebook_count = issuebook.count()
    total_books = Books.objects.count()

    context = {'issuebook_count':issuebook_count,'total_books':total_books}
    return render(request, 'issue_book_to_student.html', context)

def issue_book_to_student(request):
    issuebook = IssueBook.objects.filter(user_id=request.user.id)
    context = {'issuebook':issuebook}
    return render(request,'issued_book_to_student.html',context)

def booklisttostudnet(request):
    books, search_book = searchbooks(request)
    custom_range,  books = paginateBooks(request, books, 5)

    context ={"books":books,'search_book':search_book,'custom_range':custom_range}
    return render(request, 'book_list_to_student.html',context)

def return_date(request,id): 
    if request.method == 'POST':
        issuebook = IssueBook.objects.get(pk=id)
        returned_date = request.POST.get('returned_date')
        issuebook.returned_date = returned_date
        book = Books.objects.get(pk=issuebook.book_id.id)
        book.available_quantity = book.available_quantity + 1
        issuebook.save()
        book.save()

        return redirect('view-issuebook',books='all')
    else:
        
        return redirect('view-issuebook',books='all') 

def like(request, book_id, like):
    user = request.user
    book = Books.objects.get(pk=book_id)
    liked = StudentBook.objects.filter(user_id=user,book_id=book).count()

    if not liked:
        StudentBook.objects.create(user_id=user,book_id=book, is_liked=like)
    else:
        liked = StudentBook.objects.filter(user_id=user,book_id=book).first()
        if like == 1:
            liked.is_liked = 1
            liked.save()
        else:
            liked.is_liked = 0
            liked.save()
    
    return redirect('books-page')

def favourite(request, book_id, favourite):
    user = request.user
    book = Books.objects.get(pk=book_id)
    record = StudentBook.objects.filter(user_id=user,book_id=book).count()

    if not record:
        StudentBook.objects.create(user_id=user,book_id=book, is_favourite=favourite)
    else:
        record = StudentBook.objects.filter(user_id=user,book_id=book).first()
        if favourite == 1:
            record.is_favourite = 1
            record.save()
        else:
            record.is_favourite = 0
            record.save()
    return redirect('books-page')

def BooksPage(request):
    books, search_book = searchbooks(request)
    custom_range,  books= paginateBooks(request, books, 6)
    for book in books:
        record = StudentBook.objects.filter(user_id=request.user,book_id=book).first()
        if not record:
            book.is_liked = False
            book.is_favourite = False
        else:
            book.is_liked = record.is_liked
            book.is_favourite = record.is_favourite

    context = {'books':books,'search_book':search_book, 'custom_range':custom_range}
    return render(request, 'books.html', context)

def MyFavourites(request):
    favourite_books_ids = StudentBook.objects.filter(user_id=request.user, is_favourite=1).values_list('book_id', flat=True)
    books = Books.objects.filter(pk__in=favourite_books_ids)

    for book in books:
        record = StudentBook.objects.filter(user_id=request.user,book_id=book).first()
        if not record:
            book.is_liked = False
            book.is_favourite = False
        else:
            book.is_liked = record.is_liked
            book.is_favourite = record.is_favourite

    context = {'books': books}
    return render(request, 'my_books.html', context)