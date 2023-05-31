from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *
from .forms import BookForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenicated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from django.db.models import Q
from .utils import searchbooks, paginateBooks
from django.urls import reverse
from django.contrib import messages
from .signals import *


# Create your views here.


@login_required(login_url='login-page')
@admin_only
def Admin(request):
    return render(request, 'home.html')

# Books Management
@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def book_list(request):
    books = Books.objects.all()
    context = {'books': books}
    return render(request, 'book_list.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def add_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        form.save()
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


# Users Managements
@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login-page')
def user_list(request):
    users = User.objects.all()
    context = {'users': users}
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

    context = {'form': form}
    return render(request, 'register_page.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login-page')

def Profile(request):
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

    context = {'books': books, 'search_book': search_book,
               'custom_range': custom_range}
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

