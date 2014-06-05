from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from .utils import authenticate, check_expiration
from django.http import HttpResponse
import json

def require_login(func):
    """require_login decorator function"""
    def _require_login(request, *args, **kwargs):
        if request.session.get("username", None) == None:
            # if request is ajax return json
            if request.is_ajax() == True:
                retval = {'retval':'failed', 'data':'require login!'}
                return HttpResponse(json.dumps(retval, ensure_ascii=False))
            return render(request, "auth/login.html",
                          {"message":'Need authenticate!',
                           "redirect":request.build_absolute_uri})
        # if token is expired go to login
        #auth_ref = request.session.get("auth_ref", None)
        #try:
        #    expires_at = auth_ref['expires_at']
        #    print expires_at
        #    if check_expiration(expires_at) == True:
        #        pass
        #    else:
        #        return render(request, "auth/login.html",
        #                        {"message":'Token Expired!',
        #                        "redirect":request.build_absolute_uri})

        #except Exception, e:
        #    return render(request, "auth/login.html",
        #                  {"message":'Error!'+e.message,
        #                   "redirect":request.build_absolute_uri})
        ret = func(request, *args, **kwargs)
        return ret
    return _require_login


def login(request):
    """login"""
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        redirect_url = request.GET.get("redirect", None)

        result = authenticate(username=username, password=password)
        if result["result"] is True:
            request.session['username'] = username
            request.session['password'] = password
            request.session['auth_ref'] = result['client'].auth_ref
            if redirect_url == None or redirect_url == "":
                return redirect(reverse("project", args=("overview",)))
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


class User(object):
    def __init__(self, auth_ref, **kvargs):
        self.username = auth_ref.username
        self.auth_token = auth_ref.auth_token
        self.scoped = auth_ref.scoped
        self.project_id = auth_ref.project_id
        self.role_names = auth_ref.rolen_names
