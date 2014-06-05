from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('dashboard_auth.urls', namespace="dashboard_auth")),
    url(r'^project/(?P<optype>\w+)/$', 'dashboard.views.project', name='project'),
    url(r'^project/$', 'dashboard.views.default', name='default'),
    url(r'^settings/$', 'dashboard.views.settings', name='settings'),
    url(r'^helps/$', 'dashboard.views.helps', name='helps'),
    #url(r'^keystone/get_tenant_list/$', 'dashboard.views.get_tenant_list', name='get_tenant_list'),
    #url(r'^nova/get_flavor_list/$', 'dashboard.views.get_flavor_list', name='get_flavor_list'),
    #url(r'^nova/get_server_list/$', 'dashboard.views.get_server_list', name='get_server_list'),
    #url(r'^nova/create_server/$', 'dashboard.views.create_server', name='create_server'),
    #url(r'^nova/delete_server/$', 'dashboard.views.delete_server', name='delete_server'),
#)
#) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
) + staticfiles_urlpatterns()
