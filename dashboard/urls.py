# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^auth/', include('dashboard_auth.urls', namespace="dashboard_auth")),

    # project 为公司管理员界面
    url(r'^project/(?P<optype>\w+)/$',
        'dashboard.views.project',
        name='project'),

    url(r'^project/$',
        'dashboard.views.project_default',
        name='project_default'),

    # admin 为系统管理员界面
    url(r'^admin/(?P<optype>\w+)/$',
        'dashboard.adminviews.admin',
        name='admin'),

    url(r'^admin/$',
        'dashboard.adminviews.admin_default',
        name='project_default'),

    url(r'^settings/$', 'dashboard.views.dashboard_settings', name='settings'),
    url(r'^helps/$', 'dashboard.views.helps', name='helps'),


    #url(r'^keystone/get_tenant_list/$', 'dashboard.views.get_tenant_list', name='get_tenant_list'),
    #url(r'^nova/get_flavor_list/$', 'dashboard.views.get_flavor_list', name='get_flavor_list'),
    #url(r'^nova/get_server_list/$', 'dashboard.views.get_server_list', name='get_server_list'),
    #url(r'^nova/create_server/$', 'dashboard.views.create_server', name='create_server'),
    #url(r'^nova/delete_server/$', 'dashboard.views.delete_server', name='delete_server'),

    ##################################
    # 所有ajax请求都通过api接口进行操作
    ##################################
    url(r'^api/admin/create_project/', ''),


    # desktop
    url(r'^desktop/create_server/$', 'dashboard.views.desktop_create_server',
        name='desktop_create_server'),
    url(r'^desktop/delete_server/$', 'dashboard.views.desktop_delete_server',
        name='desktop_delete_server'),

    # users
    url(r'^users/create_user/$', 'dashboard.views.users_create_user',
        name='users_create_user'),
    url(r'^users/active_user/$', 'dashboard.views.users_active_user',
        name='users_active_user'),
    url(r'^users/delete_user/$', 'dashboard.views.users_delete_user',
        name='users_delete_user'),

    #tenants
    url(r'^tenants/create_tenant/$', 'dashboard.views.tenants_create_tenant',
        name='tenants_create_tenant'),
    url(r'^tenants/delete_tenant/$', 'dashboard.views.tenants_delete_tenant',
        name='tenants_delete_tenant'),
#)
#) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
) + staticfiles_urlpatterns()
