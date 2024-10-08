from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenicated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('admin-page')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.group:
                group = request.user.group.name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Your are not authorized to view this page!')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.group:
            group = request.user.group.name
        if group == 'student':
            return redirect('view-issue-to-student')
        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function
