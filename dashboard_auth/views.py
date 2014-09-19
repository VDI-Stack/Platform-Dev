# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from .models import User, Group

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

from django.contrib import messages as django_messages

from keystoneclient.v2_0.client import Client as keystone_client
from dashboard.settings import AUTH_URL_V2
from keystoneclient import exceptions as keystone_exceptions

# from .utils import authenticate, check_expiration
from django.http import HttpResponse
import json

def require_login(func):
    """require_login decorator function"""
    def _require_login(request, *args, **kwargs):
        if request.session.get("username", None) is None:
            # if request is ajax return json
            if request.is_ajax() is True:
                retval = {'retval': 'failed', 'data': 'require login!'}
                return HttpResponse(json.dumps(retval, ensure_ascii=False))
            django_messages.add_message(
                request,
                50,
                "Please login first! ",
                extra_tags="danger")
            return redirect(reverse(
                "dashboard_auth:login") +
                "?redirect="+request.build_absolute_uri())

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


def require_permission(permission):
    """require_permission decorator function"""
    def _require_permission(func):
        def __require_permission(request, *args, **kwargs):
            if request.session.get("permission", None) is None:
                django_messages.add_message(
                    request,
                    50,
                    "Please login first! ",
                    extra_tags="danger")
                return redirect(reverse(
                    "dashboard_auth:login") +
                    "?redirect="+request.build_absolute_uri())
            if permission == request.session.get("permission"):
                return func(request, *args, **kwargs)
            else:
                django_messages.add_message(
                    request,
                    50,
                    "Permission deny! ",
                    extra_tags="danger")
                return redirect(reverse(
                    "dashboard_auth:login") +
                    "?redirect="+request.build_absolute_uri())

        return __require_permission
    return _require_permission


def splash(user):
    return redirect(reverse("project", args=("overview",)))


def check_group(groupname):
    try:
        group1 = Group.objects.get(enable=1, name=groupname)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        print "Group %s ,\
            ObjectDoesNotExist or MultipleObjectsReturned!" % groupname
        return None
    return group1


def check_user(username, groupid):
    try:
        user1 = User.objects.get(enable=1, name=username, groupid=groupid)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        print "User %s in Groupid %s, \
            UserDoesNotExist or MultipleObjectReturned!" % (username, groupid)
        return None
    return user1


def login(request):
    """login"""
    if request.method == "POST":
        input_name = request.POST.get("username", None)
        input_password = request.POST.get("password", None)
        redirect_url = request.GET.get("redirect", None)

        input_len = len(input_name.split('@'))
        if input_len == 2:
            # 1 普通用户
            username, groupname = input_name.split('@')
            # print username, groupname
            # 1.1检查组
            group1 = check_group(groupname)
            if group1 is None:
                django_messages.add_message(
                    request,
                    50,
                    '@%s,%s is not exist or MultiGroupExist!' %
                    (groupname, groupname),
                    extra_tags="danger")
                return render(request, "auth/login.html", {
                    'username': input_name,
                    'redirect': redirect_url,
                    })
            # 1.2检查用户密码
            user1 = check_user(username, group1.id)
            if user1 is None:
                django_messages.add_message(
                    request,
                    50,
                    '%s@%s, username %s is not exist in %s or MultiUserExist!'
                    % (username, groupname, username, groupname),
                    extra_tags="danger")
                return render(request, "auth/login.html", {
                    'username': input_name,
                    'redirect': redirect_url,
                    })
            if user1.check_password(input_password) is True:
                request.session['username'] = username
                request.session['password'] = input_password
                request.session['groupname'] = groupname
                request.session['groupid'] = group1.id
                request.session['tenantid'] = group1.tenantid
                request.session['permission'] = '3'
                # 1.3 进入用户管理界面
                return redirect(reverse("project", args=("overview",)))
            else:
                django_messages.add_message(
                    request,
                    50,
                    'Invalid password',
                    extra_tags="danger")
                return render(request, "auth/login.html", {
                    'username': input_name,
                    'redirect': redirect_url,
                    })

        elif input_len == 1:
            # 2 管理员用户
            # 使用keystone的用户认证和管理
            try:
                # 采取管理员用户名和project(tenant)名相同的模式
                # 对于admin用户必须存在相应的admin tenant
                tenant_name = input_name

                keystone_client_1 = keystone_client(
                    username=input_name,
                    password=input_password,
                    tenant_name=tenant_name,
                    auth_url=AUTH_URL_V2)
                request.session['username'] = input_name
                request.session['tenant_name'] = tenant_name
                request.session['password'] = input_password
            except (keystone_exceptions.Unauthorized,
                    keystone_exceptions.Forbidden,
                    keystone_exceptions.NotFound) as exc:
                print exc.message
                msg = 'Invalid user name or password.'
                django_messages.add_message(
                    request,
                    50,
                    msg,
                    extra_tags="danger")
                return render(request, "auth/login.html", {
                    'username': input_name,
                    'redirect': redirect_url,
                    })
            except (keystone_exceptions.ClientException,
                    keystone_exceptions.AuthorizationFailure) as exc:
                print exc.message
                django_messages.add_message(
                    request,
                    50,
                    'Invalid user name or password',
                    extra_tags="danger")
                return render(request, "auth/login.html", {
                    'username': input_name,
                    'redirect': redirect_url,
                    })
            if input_name == "admin":
                # 2.1 进入admin管理界面
                request.session['permission'] = '1'
                return redirect(reverse("admin", args=("overview",)))
            else:
                # 2.2 进入普通管理员界面
                request.session['permission'] = '2'
                return redirect(reverse("project", args=("overview",)))
        else:
            # error
            print "input_len unexception!"
            pass
        #try:
        #    keystone_client_1 = \
        #        keystone_client(username=username,
        #            password=password,
        #            tenant_name=tenant_name,
        #            auth_url=AUTH_URL_V2)
        #result = authenticate(username=username, password=password)
        #if result["result"] is True:
        #    request.session['username'] = username
        #    request.session['password'] = password
        #    request.session['auth_ref'] = result['client'].auth_ref
        #    if redirect_url is None or redirect_url == "":
        #        return redirect(reverse("project", args=("overview",)))
        #    else:
        #        return redirect(redirect_url)
        #else:
        #    print result["message"]
        #    return render(request, "auth/login.html", {
        #        'message': result["message"],
        #        'username': username,
        #        'redirect': redirect_url,
        #    })
    username = request.session.get("username", "")
    return render(request, "auth/login.html", {'username': username})


def logout(request):
    """logout"""
    request.session.clear()
    request.session.clear_expired()
    return redirect(reverse("dashboard_auth:login"))


#class User(object):
#    def __init__(self, auth_ref, **kvargs):
#        self.username = auth_ref.username
#        self.auth_token = auth_ref.auth_token
#        self.scoped = auth_ref.scoped
#        self.project_id = auth_ref.project_id
#        self.role_names = auth_ref.rolen_names
