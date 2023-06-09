from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import *
from .forms import BookForm,CategoryForm,AuthorForm,CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenicated_user, allowed_users, admin_only
from .utils import searchbooks, paginateBooks,searchuser,paginateUsers
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .signals import *
from django.db.models import Q
from django.contrib.auth.models import User,Group



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
    deadline_returns_book = IssueBook.objects.filter(expected_return_date__lte= five_days_later, expected_return_date__gt=today)
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
    return redirect('books-management')

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def booksnotreturnyet(request):
    today = timezone.now().date()
    five_days_later = today + timedelta(days=7)
    deadline_returns_book = IssueBook.objects.filter(expected_return_date__lte= five_days_later, expected_return_date__gt=today)

    context={'deadline_returns_book':deadline_returns_book}
    return render(request,'books_not_return.html',context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def issue_book(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        expected_return_date = request.POST.get('expected_return_date')
        
        user = User.objects.get(pk=user_id)
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
        users = User.objects.all()
        books = Books.objects.filter(available_quantity__gt= 0 )
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
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            role_group = request.POST['group'].lower()
            group = Group.objects.get(name=role_group)
            user.groups.add(group)

        messages.success(request,"User successfully added")
        return redirect('users-management')

    context = {'form': form}
    return render(request, 'add_user.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def Update_user(request, id):
    if request.method == 'POST':
        user = User.objects.get(pk=id)
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()

            role_group = request.POST['group'].lower()
            group = Group.objects.get(name=role_group)
            user.groups.add(group)

        return redirect('users-management')
    else:
        user = User.objects.get(pk=id)
        form = CreateUserForm(instance=user)

    context = {'form': form, 'user_group' : user.groups.get}
    return render(request, 'update_user.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def Delete_user(request, id):
    users = User.objects.get(pk=id)
    users.delete()
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
            messages.info(request, 'Username or Password is incorrect!')

    context = {}
    return render(request, 'index.html', context)


@unauthenicated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':

        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='student')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login-page')
    context = {'form':form}
    return render(request,'register_page.html',context)
   

def logoutUser(request):
    logout(request)
    return redirect('login-page')

def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            form = CreateUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                login(request, user)
            return redirect('user-profile')
        else:
            user = request.user
            form = CreateUserForm(instance=user)

        context = {'form': form, 'user_group' : user.groups.get}
        return render(request, 'user_profile.html', context)
    else:
        return redirect('login-page')

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

