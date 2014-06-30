#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from dashboard_auth.views import require_login
from dashboard_auth.utils import authenticate
from dashboard.api.keystone import get_tenant_list as keystone_get_tenant_list
from dashboard.api.nova import get_nova_client as nova_get_nova_client
from dashboard.api.nova import Server as NovaServer
from dashboard import settings
from dashboard.utils import get_default_panel_url
from dashboard.utils import nova_create_server
from novaclient.client import Client as nova_client
from keystoneclient.v2_0 import Client as KeystoneClientV2
from keystoneclient.v2_0 import Client as keystone_client

import json

AUTH_URL = settings.AUTH_URL
AUTH_URL_V2 = settings.AUTH_URL_V2

@require_login
def default(request):
    return redirect(get_default_panel_url())

@require_login
def project(request, optype):
    """project request"""
    username = request.session.get("username", None)
    auth_ref = request.session.get("auth_ref", None)
    current_project_name = request.session.get("project_name", None)
    current_project_id = request.session.get("project_id", None)

    auth_result = authenticate(token=auth_ref['auth_token'],
                            project_name=current_project_name,
                            auth_url=AUTH_URL)

    if auth_result['result'] == False:
        print ("failed! project authenticate!"+auth_result['message'])
        return redirect(reverse('dashboard_auth:login'))
    else:
        c = auth_result['client']

    project_list = c.projects.list(user=c.user_id)
    if len(project_list) == 0:
        return HttpResponse("user don't have project")
    current_project_name = c.project_name


    #TODO:if is unscoped!
    request.session['project_name'] = c.project_name
    request.session['project_id'] = c.project_id

    switch = request.GET.get("switch", None)
    if switch != None:
        for index in project_list:
            if switch == index.name:
                auth_result = authenticate(token=auth_ref['auth_token'],
                                           project_name=index.name,
                                           auth_url=AUTH_URL)
                if auth_result['result'] == False:
                    print auth_result['message']
                    return HttpResponse("failed!")
                else:
                    request.session['project_name'] = \
                        auth_result['client'].project_name
                    request.session['project_id'] = \
                        auth_result['client'].project_id
                    return redirect(get_default_panel_url())

    return route_to(optype,
                  request,
                  "project.html",
                  {
                      "username":username,
                      "project_list":project_list,
                      "current_project_name":current_project_name,
                      "keystone_client":c,
                  })



def test1(request, template_name, template_data):
    return render(request, template_name, template_data)


def overview(request, template_name, template_data):
    """overview页面"""
    return render(request, "overview.html", template_data)


def desktop(request, template_name, template_data):
    """云桌面的内容的函数"""
    username = request.session.get("username", None)
    password = request.session.get("password", None)
    project_name = request.session.get("project_name", None)
    auth_ref = request.session.get("auth_ref", None)
    try:
        c = nova_client(3, username, password,
                        project_name, AUTH_URL_V2)
    except Exception, e:
        return HttpResponse(e.msg)

    servers = []
    for s in c.servers.list():
        servers.append(NovaServer(s, auth_ref, c))
    template_data['servers'] = servers
    return render(request, "desktop.html", template_data)


def manage_users(request, template_name, template_data):
    username = request.session.get("username", None)
    password = request.session.get("password", None)
    project_name = request.session.get("project_name", None)
    auth_ref = request.session.get("auth_ref", None)

    try:
        keystone_c = template_data['keystone_client']
    except Exception, e:
        print e.message
        return HttpResponse("failed get keystone client in template_data!")
    users = keystone_c.users.list()
    #users.sort(lambda p1, p2: cmp(p1.name, p2.name))

    template_data['users'] = users

    return render(request, "users.html", template_data)


def manage_tenants(request, template_name, template_data):
    """tenants 管理"""
    username = request.session.get("username", None)
    password = request.session.get("password", None)
    project_name = request.session.get("project_name", None)
    auth_ref = request.session.get("auth_ref", None)

    try:
        keystone_client_1 = template_data['keystone_client']
    except Exception, e:
        print e.message
        return HttpResponse("failed get keystone client in template_data!")

    tenants = []
    try:
        for tenant in keystone_client_1.projects.list():
            tenants.append({"id":tenant.id, "name":tenant.name})
    except Exception, e:
        print e.message
        return HttpResponse("failed! " + e.message)
    #print tenants
    template_data['tenants'] = tenants

    return render(request, "tenants.html", template_data)

def route_to(optype, request, template_name, template_data):
    """对于不同的路径进行不同的函数调用"""
    template_data['optype'] = optype
    return {
        'test':test1,
        'overview':overview,
        'desktop':desktop,
        'users':manage_users,
        'tenants':manage_tenants,
    }[optype](request, template_name, template_data)


def dashboard_settings(request):
    """settings"""
    return HttpResponse("Settings")


def helps(request):
    """helps"""
    return HttpResponse("Helps")


@require_login
def desktop_create_server(request):
    """创建虚拟机"""
    username = request.session.get("username", None)
    password = request.session.get("password", None)
    project_name = request.session.get("project_name", None)
    auth_ref = request.session.get("auth_ref", None)
    try:
        c = nova_client(2, username, password,
                        project_name, AUTH_URL_V2)
    except Exception, e:
        # 返回错误对话框，点击后跳转到登陆
        print e.msg
        return HttpResponse(e.msg)

    if request.method == 'POST':
        print request.POST.get('inputServerName', None)
        print request.POST.get('inputServerFlavor', None)
        print request.POST.get('inputServerCount', 0)
        print request.POST.get('inputServerBootType', None)
        print request.POST.get('inputServerImage', None)

        res = nova_create_server(request, c)
        if res['result'] == True:
            retval = {'retval':'success', 'data':'ok'}
        else:
            retval = {'retval':'failed', 'data':'failed'}
        return HttpResponse(json.dumps(retval, ensure_ascii=False))


    flavors = []
    for flavor in c.flavors.list():
        flavors.append({
            'name':flavor.name,
            'id':flavor.id
        })

    images = []
    for image in c.images.list():
        images.append({
            'name':image.name,
            'id':image.id
        })

    return render(request,
                  "create_server.html",
                  {
                      'flavors':flavors,
                      'images':images,
                  })


@require_login
def desktop_delete_server(request):
    print "desktop delete server"
    if request.method == "POST":

        username = request.session.get("username", None)
        password = request.session.get("password", None)
        project_name = request.session.get("project_name", None)
        auth_ref = request.session.get("auth_ref", None)
        delete_server_list = request.POST.getlist("selectuser")
        print delete_server_list
        try:
            c = nova_client(2, username, password,
                             project_name, AUTH_URL_V2)
            #c.servers.delete()

        except Exception, e:
            print e.message
            pass

    retval = {'retval':'success', 'data':'ok'}

    return HttpResponse(json.dumps(retval, ensure_ascii=False))


@require_login
def users_create_user(request):
    """创建用户"""
    if request.method == "POST":
        input_name = request.POST.get('inputName', None)
        input_email = request.POST.get('inputEmail', None)
        input_tenant = request.POST.get('inputTenant', None)

        auth_ref = request.session.get('auth_ref', None)
        username = request.session.get('username', None)
        password = request.session.get('password', None)
        current_project_name = request.session.get('project_name', None)

        try:
            keystone_client_1 = KeystoneClientV2(username=username,
                                               password=password,
                                               tenant_name=current_project_name,
                                               auth_url=AUTH_URL_V2)
            user_manager_1 = keystone_client_1.users
            user1 = user_manager_1.create(name=input_name,
                                  password="123456",
                                  tenant_id=input_tenant,
                                  email=input_email)
            retval = {'retval':'success', 'data':'ok'}
        except Exception, e:
            retval = {'retval':'failed', 'data':'create user failed'}
            print e.message


        return HttpResponse(json.dumps(retval, ensure_ascii=False))

    elif request.method == "GET":
        auth_ref = request.session.get('auth_ref', None)
        current_project_name = request.session.get('project_name', None)

        auth_result = authenticate(token=auth_ref['auth_token'],
                            project_name=current_project_name,
                            auth_url=AUTH_URL)
        tenants = []
        if auth_result['result'] == True:
            keystone_client_1 = auth_result['client']
            tenant_manager_1 = keystone_client_1.projects
            for tenant in tenant_manager_1.list():
                tenants.append({"id":tenant.id, "name":tenant.name})
            return render(request,
                          'create_user.html',
                          {
                              'tenants':tenants,
                          })
        else:
            return render(request,
                          'create_user.html',
                          {
                          })

    else:
        pass
    return render(request,
                  'create_user.html',
                  {
                  })


@require_login
def users_delete_user(request):
    """delete user"""
    if request.method == "POST":
        username = request.session.get("username", None)
        password = request.session.get("password", None)
        current_project_name = \
            request.session.get("project_name", None)
        keystone_client_1 = \
            keystone_client(username=username,
                            password=password,
                            tenant_name=current_project_name,
                            auth_url=AUTH_URL_V2)
        for user_id in request.POST.getlist("selectuser", None):
            #print user_id
            keystone_client_1.users.delete(user_id)

        retval = {'retval':'success', 'data':'ok'}
        return HttpResponse(json.dumps(retval, ensure_ascii=False))

@require_login
def users_active_user(request):
    """激活用户"""
    if request.method == "POST":
        print request.POST.getlist('selectusers', None)
        retval = {'retval':'success', 'data':"ok"}
        return HttpResponse(json.dumps(retval, ensure_ascii=False))
    return HttpResponse("not support")


###
@require_login
def get_tenant_list(request):
    """get tenant list"""
    if request.is_ajax() == True and request.method == "POST":
        username = request.session.get("username", None)
        password = request.session.get("password", None)



        tenant_list = keystone_get_tenant_list(AUTH_URL, username, password)
        tenants = []
        for tenant in tenant_list:

            tenants.append({'name':tenant.name, 'id':tenant.id})

        retval = {'retval':'success', 'data':tenants}
        return HttpResponse(json.dumps(retval, ensure_ascii=False))
    return HttpResponse("failed!")


@require_login
def tenants_create_tenant(request):
    if request.method == "GET":
        return render(request,
                      'create_tenant.html',
                      {
                      })
    elif request.method == "POST":
        auth_ref = request.session.get('auth_ref', None)
        username = request.session.get('username', None)
        password = request.session.get('password', None)
        current_project_name = request.session.get('project_name', None)

        input_name = request.POST.get('inputName', None)
        input_description = request.POST.get('inputDescription', None)

        try:
            keystone_client_1 = \
                    keystone_client(username=username,
                                    password=password,
                                    tenant_name=current_project_name,
                                    auth_url=AUTH_URL_V2)
            tenant_1 = keystone_client_1.tenants.create(input_name,
                                             input_description,
                                             True)
        except Exception, e:
            print e.message
            retval = {'retval':'failed', 'data':'failed'}

        retval = {'retval':'success', 'data':'ok'}
        return HttpResponse(json.dumps(retval, ensure_ascii=False))
    else:
        return HttpResponse("not support other method")


@require_login
def tenants_delete_tenant(request):
    """delete tenant """
    if request.method == "POST":
        username = request.session.get("username", None)
        password = request.session.get("password", None)
        current_project_name = \
            request.session.get("project_name", None)
        keystone_client_1 = \
            keystone_client(username=username,
                            password=password,
                            tenant_name=current_project_name,
                            auth_url=AUTH_URL_V2)
        for tenant_id in request.POST.getlist("selectuser", None):
            keystone_client_1.tenants.delete(tenant_id)

        retval = {'retval':'success', 'data':'ok'}
        return HttpResponse(json.dumps(retval, ensure_ascii=False))


@require_login
def get_flavor_list(request):
    """get nova flavor list"""
    if request.is_ajax() == True and request.method == "POST":
        username = request.session.get("username", None)
        password = request.session.get("password", None)
        current_tenant_name = request.session.get("tenant_name", None)

        result = nova_get_nova_client(username,
                                 password,
                                 current_tenant_name,
                                 AUTH_URL)
        if result["result"] == False:
            return HttpResponse("failed! "+result["message"])
        else:
            nova_c = result["client"]
            flavors = []
            for flavor in nova_c.flavors.list():
                flavors.append({'name':flavor.name, 'id':flavor.id})
            retval = {'retval':'success', 'data':flavors}
            return HttpResponse(json.dumps(retval, ensure_ascii=False))
    return HttpResponse("failed!")


@require_login
def get_server_list(request):
    """get nova server list"""
    if request.is_ajax() == True and request.method == "POST":
        username = request.session.get("username", None)
        password = request.session.get("password", None)
        current_tenant_name = request.session.get("tenant_name", None)
        result = nova_get_nova_client(username,
                                 password,
                                 current_tenant_name,
                                 AUTH_URL)
        if result["result"] == False:
            return HttpResponse("failed! "+result["message"])
        else:
            nova_c = result["client"]
            servers = []
            for server in nova_c.servers.list():
                servers.append({'name':server.name, 'id':server.id})
            retval = {'retval':'success', 'data':servers}
            return HttpResponse(json.dumps(retval, ensure_ascii=False))
    return HttpResponse("failed!")


@require_login
def create_server(request):
    """create nova server"""
    if request.is_ajax() == True and request.method == "GET":
        username = request.session.get("username", None)
        password = request.session.get("password", None)
        current_tenant_name = request.session.get("tenant_name", None)
        result = nova_get_nova_client(username,
                                 password,
                                 current_tenant_name,
                                 AUTH_URL)
        if result["result"] == False:
            return HttpResponse("failed! "+result["message"])
        else:
            nova_c = result["client"]
            flavors = []
            images = []
            flavors = nova_c.flavors.list()
            images = nova_c.images.list()
            #for image in nova_c.images.list():
            #    images.append({''})
        return render(request, "create_server.html",
                      {"flavors":flavors,
                       "images":images,
                       })
    elif request.method == "POST":
        name = request.POST.get('name', None)
        image_id = request.POST.get('image_id', None)
        flavor_id = request.POST.get('flavor_id', None)

        username = request.session.get("username", None)
        password = request.session.get("password", None)
        current_tenant_name = request.session.get("tenant_name", None)
        result = nova_get_nova_client(username,
                                 password,
                                 current_tenant_name,
                                 AUTH_URL)
        if result["result"] == False:
            return HttpResponse("failed!"+result["message"])
        else:
            nova_c = result["client"]
            try:
                nova_c.servers.create(name, image_id, flavor_id)
                retval = {'retval':'success'}
                return HttpResponse(json.dumps(retval, ensure_ascii=False))
            except Exception, e:
                retval = {'retval':'failed', 'message':e.message}
                return HttpResponse(json.dumps(retval, ensure_ascii=False))
        return HttpResponse("failed!")


@require_login
def delete_server(request):
    """delete nova server"""
    if request.is_ajax() == True and request.method == "POST":

        delete_servers = request.POST.getlist('list[]', None)
        username = request.session.get("username", None)
        password = request.session.get("password", None)
        current_tenant_name = request.session.get("tenant_name", None)
        result = nova_get_nova_client(username,
                                 password,
                                 current_tenant_name,
                                 AUTH_URL)
        if result["result"] == False:
            return HttpResponse("failed!"+result["message"])
        else:
            nova_c = result["client"]
            try:
                servers = nova_c.servers.list()
                for deleteid in delete_servers:
                    for server in servers:
                        if server.id == deleteid:
                            print deleteid
                            server.delete()
                retval = {'retval':'success'}
                return HttpResponse(json.dumps(retval, ensure_ascii=False))
            except Exception, e:
                retval = {'retval':'failed', 'message':e.message}
                return HttpResponse(json.dumps(retval, ensure_ascii=False))
        return HttpResponse("failed!")

