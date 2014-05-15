from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from dashboard_auth.views import require_login
from dashboard_auth.utils import authenticate_with_tenant, authenticate
from dashboard.api.keystone import get_tenant_list as keystone_get_tenant_list

import json

AUTH_URL= "http://192.168.2.10:5000/v2.0"

@require_login
def project(request):
    """project request"""
    username = request.session.get("username", None)
    password = request.session.get("password", None)

    auth_result = authenticate(username=username,
                               password=password,
                               auth_url=AUTH_URL)
    tenant_list = keystone_get_tenant_list(AUTH_URL, username, password)

    # switch tenant
    switch = request.GET.get("switch", None)
    if switch != None:
        for tenant in tenant_list:
            if switch == tenant.name:
                request.session["tenant_name"] = tenant.name
                request.session["tenant_id"] = tenant.id
                return redirect(reverse("project"))

    # auth default tenant
    current_tenant_name = request.session.get("tenant_name", None)
    current_tenant_id = request.session.get("tenant_id", None)
    if current_tenant_name == None:
        for tenant in tenant_list:
            result = authenticate_with_tenant(
                tenant_id=tenant.id,
                token=auth_result["auth_ref"].auth_token,
                auth_url=AUTH_URL)
            if result["result"] == True:
                current_tenant_name = tenant.name
                current_tenant_id = tenant.id
                break
        if current_tenant_id == None:
            return render(request, "auth/login.html",
                          {"message":"user don't have tenants",
                           'username':username})
    else:
        result = authenticate_with_tenant(
            tenant_id=current_tenant_id,
            token=auth_result["auth_ref"].auth_token,
            auth_url=AUTH_URL)

    if result["result"] == True:
        request.session["tenant_id"] = current_tenant_id
        request.session["tenant_name"] = current_tenant_name

    # get
    tenant_name_list = []
    for tenant in tenant_list:
        tenant_name_list.append(tenant.name)

    return render(request, "project.html",
                  {"username":username,
                   "tenant_name_list":tenant_name_list,
                   "current_tenant_name":current_tenant_name})


@require_login
def get_tenant_list(request):
    """"""
    if request.is_ajax() == True and request.method == "POST":
        username = request.session.get("username", None)
        password = request.session.get("password", None)
        tenant_list = keystone_get_tenant_list(AUTH_URL, username, password)
        retval = {'retval':'123123'}
        return HttpResponse(json.dumps(retval, ensure_ascii=False))
    return HttpResponse("failed!")
