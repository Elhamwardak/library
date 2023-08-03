
from django.db.models import Q
from .models import Books, CustomUser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from celery import shared_task
from django.http import JsonResponse



def paginateBooks(request, book, results):

    page = request.GET.get('page')
    paginator = Paginator(book, results)

    try:
        book = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        book = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        book = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    return custom_range, book


def searchbooks(request):
    search_book = ''

    if request.GET.get('search_book'):
        search_book = request.GET.get('search_book')

    book = Books.objects.filter(Q(title__icontains=search_book)|
                                Q(author__name__icontains=search_book)|
                                 Q(category__name__icontains=search_book)
                                 ) 
                                
    return book, search_book

def searchuser(request):
    search_user = ''

    if request.GET.get('search_user'):
        search_user = request.GET.get('search_user')

    user = CustomUser.objects.filter(Q(username__icontains=search_user) | 
                                Q(id__icontains=search_user)
                                ) 
                                
    return user, search_user

def paginateUsers(request, users, results):

    page = request.GET.get('page')
    paginator = Paginator(users, results)

    try:
        user = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        user = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        user = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    return custom_range, user

# @shared_task
# def send_email_task(subject, message, from_email, recipient_list):
#     send_mail(
#         subject,
#         message,
#         from_email,
#         recipient_list,     
#         )
    