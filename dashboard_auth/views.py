from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from .utils import authenticate

def require_login(func):
    """require_login decorator function"""
    def _require_login(request, *args, **kwargs):
        if request.session.get("username", None) == None:
            return render(request, "auth/login.html",
                          {"message":'Need authenticate!',
                           "redirect":request.build_absolute_uri})
        ret = func(request, *args, **kwargs)
        return ret
    return _require_login


def login(request):
    """login"""
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        redirect_url = request.POST.get("redirect-url", None)

        result = authenticate(username=username, password=password)
        if result["result"] is True:
            request.session['username'] = username
            request.session['password'] = password
            if redirect_url == "":
                return redirect(reverse("project"))
            else:
                return redirect(redirect_url)
        else:
            return render(request, "auth/login.html",
                          {'message':result["message"],
                            'username':username,
                            'redirect':redirect_url,})

    return render(request, "auth/login.html")


def logout(request):
    """logout"""
    request.session.clear()
    request.session.clear_expired()
    return redirect(reverse("dashboard_auth:login"))
