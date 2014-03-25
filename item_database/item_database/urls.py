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
    url(r'^user/(?P<username>\w+).(?P<format>\w+)$', userpage),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    
    url(r'^itemclasses.(?P<format>\w+)$', itemClassListPage),
    url(r'^itemclasses/(?P<classItemID>\w+).(?P<format>\w+)$', itemClassPage),

    url(r'^areas.(?P<format>\w+)$', areaListPage),
    url(r'^areas/(?P<areaID>\w+).(?P<format>\w+)$', areaPage),

    url(r'^creatures.(?P<format>\w+)$', creatureListPage),
    url(r'^creatures/(?P<creatureID>\w+).(?P<format>\w+)$', creaturePage),

    url(r'^items.(?P<format>\w+)$', itemListPage),
    url(r'^items/(?P<itemID>\w+).(?P<format>\w+)$', itemPage),
)
