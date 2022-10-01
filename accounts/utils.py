

def detectuser(user):
    if user.role == 1:
        redirecturl = 'company-dashboard'
        return redirecturl
    elif user.role == 2:
        redirecturl = 'myaccount'
        return redirecturl
    elif user.is_superadmin:
        redirecturl = '/admin'
        return redirecturl

