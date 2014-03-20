from django.conf.urls import patterns, include, url
from iitem_database.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'item_database.views.home', name='home'),
    # url(r'^item_database/', include('item_database.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', mainpage, name='home'),
    url(r'^user/([\w ]+)/$', userpage),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^itemclasses/$', itemClassListPage),
    url(r'^itemclasses/([\w ]+)/$', itemClassPage),
    url(r'^areas/$', areaListPage),
    url(r'^areas/([\w ]+)/$', areaPage),
    url(r'^creatures/$', creatureListPage),
    url(r'^creatures/([\w ]+)/$', creaturePage),
    url(r'^items/$', itemListPage),
    url(r'^items/([\w ]+)/$', itemPage),
)
