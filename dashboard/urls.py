from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('dashboard_auth.urls')),
    url(r'^$', 'dashboard.views.project', name='project'),
#)
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

