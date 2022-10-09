from django.shortcuts import redirect
from django.contrib import messages
def login_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"You must sign in kalla vaduva")
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

def login_company_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"You must sign in kalla vaduva")
            return redirect("company-login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper