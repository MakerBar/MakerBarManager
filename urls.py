from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^SupplyRequest/$', 'MakerBarManager.SupplyRequest.views.home', name='home'),
    url(r'^presence/members_connected/$', 'MakerBarManager.presence.views.members_connected', name='members_connected'),
    url(r'^presence/who_is_connected/$', 'MakerBarManager.presence.views.who_is_connected', name='who_is_connected'),
    # url(r'^MakerBarManager/', include('MakerBarManager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment these two lines to enable your static files on PythonAnywhere
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

