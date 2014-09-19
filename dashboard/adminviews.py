# -*- coding:utf-8 -*-
from keystoneclient.v2_0.client import Client as keystone_client
from dashboard.settings import AUTH_URL_V2

from django.contrib import messages as django_messages
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from dashboard_auth.views import require_login, require_permission
from dashboard_auth.models import User, Group

@require_login
@require_permission("1")
def admin(request, optype):
    """admin 管理路径"""
    username = request.session.get("username", None)
    password = request.session.get("password", None)
    tenant_name = request.session.get("tenant_name", None)

    try:
        keystone = keystone_client(
            username=username,
            password=password,
            tenant_name=tenant_name,
            auth_url=AUTH_URL_V2)
        keystone.users.list()
    except Exception as exc:
        print exc.message
        django_messages.add_message(
            request, 50, exc.message, extra_tags="danger")
        return redirect(
            reverse("dashboard_auth:login") +
            "?redirect=" + request.build_absolute_uri())
    # django_messages.add_message(request, 50, "hello", extra_tags="success")
    # django_messages.add_message(request, 50, "hello1", extra_tags="info")
    # django_messages.add_message(request, 50, "hello2", extra_tags="danger")
    # django_messages.add_message(request, 50, "hello2", extra_tags="warning")
    return route_to(
        optype, request, "admin/overview.html", {
            "username": username,
            "tenant_name": tenant_name,
            "keystone_client": keystone,
        })


@require_login
@require_permission("1")
def admin_default(request):
    return redirect(reverse("admin", args=("overview",)))


def route_to(optype, request, template_name, template_data):
    template_data['optype'] = optype
    try:
        return {
            'overview': overview,
            'project': manage_project,
            'add_project': add_project,
        }[optype](request, template_name, template_data)
    except KeyError:
        print "Admin KeyError! %s not found!" % optype
        return redirect(reverse("admin", args=('overview',)))


def overview(request, template_name, template_data):
    """admin overview"""

    return render(request, "admin/overview.html", template_data)


def manage_project(request, template_name, template_data):
    try:
        groups_num = Group.objects.filter(enable="1").count()
        groups = Group.objects.filter(enable="1")
        template_data['groups'] = groups
        template_data['groups_num'] = groups_num
    except Exception as exc:
        print exc.message
        msg = "查询数据库出错"
        django_messages.add_message(
            request, 50,
            msg,
            extra_tags="danger")
    return render(request, "admin/project.html", template_data)


def add_project(request, template_name, template_data):
    """创建项目"""
    keystone = template_data['keystone_client']
    return render(
        request, "admin/add_project.html",
        {
        })
