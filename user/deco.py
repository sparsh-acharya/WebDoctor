from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse


def unauthorizedUser(func):
    def wrap(request, *args, **kwargs):
        grp = None
        if request.user.is_authenticated:
            grp = request.user.groups.all()[0].name
            return redirect(grp)

        return func(request, *args, **kwargs)

    return wrap


def allowedUsers(list=[]):
    def check(func):
        def wrap(request, *args, **kwargs):
            grp = None
            if request.user.groups.exists():
                grp = request.user.groups.all()[0].name
            if grp in list:
                return func(request, *args, **kwargs)
            return redirect(grp)

        return wrap

    return check


# def notAllowedUsers(list = []):
#     def check(func):
#         def wrap(request,*args,**kwargs):
#             grp = None
#             if request.user.groups.exists():
#                 grp = request.user.groups.all()[0].name
#             if grp not in list:
#                 return func(request,*args,**kwargs)
#             return HttpResponse('Only Patients and New Users Can acess')
#         return wrap
#     return check
